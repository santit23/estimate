from config_rates import MATERIAL_RATES
from config_formulas import WINDOW_FORMULAS
from config_categories import ITEM_CATEGORY_MAP

class EstimationEngine:
    def __init__(self, series, quality):
        self.series = series
        self.quality = quality
        
        # Load the whole block (Config + Rates)
        try:
            data = MATERIAL_RATES[series][quality]
            self.rate_config = data['config'] # {'profile_unit': '20ft', ...}
            self.prices = data['rates']       # {'topfr': 1200, ...}
        except KeyError:
            raise ValueError(f"No data found for {series} {quality}")

    def calculate(self, design_type, width_ft, height_ft, quantity=1, has_mesh=False, 
                  variable_inputs=None):
        
        vars = variable_inputs or {}
        # wastage_pct = vars.get('wastage_percent', 0.0)
        labour_rate = vars.get('labour_rate_sqft', 0.0)
        transport_cost = vars.get('transport_cost', 0.0)
        profit_pct = vars.get('profit_percent', 0.0)
        glass_override = vars.get('glass_price', 0.0)

        if design_type not in WINDOW_FORMULAS:
            raise ValueError(f"Unknown design type: {design_type}")
        
        active_formulas = WINDOW_FORMULAS[design_type]
        material_breakdown = []
        net_material_cost = 0
        total_sqft = width_ft * height_ft * quantity

        for material, calc_func in active_formulas.items():
            
            if "jali" in material and not has_mesh: continue
            if material == 'labour': continue

            # 1. Get Category (e.g., 'profile', 'hardware')
            category = ITEM_CATEGORY_MAP.get(material, 'other')
            
            # 2. Get Unit Setting for this Category (e.g., '20ft')
            # We construct the key: 'profile' + '_unit' = 'profile_unit'
            config_key = f"{category}_unit"
            unit_type = self.rate_config.get(config_key, 'nos') # Default to nos if missing

            # 3. Get Price
            raw_price = self.prices.get(material, 0)
            if raw_price == 0: continue

            # 4. Math Conversion Logic
            effective_rate = raw_price
            
            if unit_type == '20ft':
                effective_rate = raw_price / 20.0
            elif unit_type == '12ft':
                effective_rate = raw_price / 12.0
            # 'ft', 'sqft', 'nos' need no divisor (effective_rate = raw_price)

            # 5. Calculate
            qty_required = calc_func(width_ft, height_ft) * quantity
            cost = qty_required * effective_rate
            
            material_breakdown.append({
                "item": material,
                "qty": round(qty_required, 2),
                "unit": unit_type,       # Display the GLOBAL unit setting
                "rate": round(raw_price, 2),
                "amount": round(cost, 2)
            })
            net_material_cost += cost

        # --- FINANCIALS (Same as before) ---
        # wastage_amount = net_material_cost * (wastage_pct / 100)
        
        if labour_rate == 0.0:
            labour_rate = self.prices.get('labour', 0)
            
        labour_cost = total_sqft * labour_rate
        production_cost = net_material_cost  + labour_cost
        cost_with_transport = production_cost + transport_cost
        profit_amount = cost_with_transport * (profit_pct / 100)
        final_price = cost_with_transport + profit_amount

        return {
            "breakdown": material_breakdown,
            "financials": {
                "1_net_material": round(net_material_cost, 2),
                # "2_wastage_amt": round(wastage_amount, 2),
                "3_labour_cost": round(labour_cost, 2),
                "4_transport": round(transport_cost, 2),
                "5_total_cost": round(cost_with_transport, 2),
                "6_profit_amt": round(profit_amount, 2),
                "7_final_price": round(final_price, 2)
            },
            "inputs": {
                # "wastage_percent": wastage_pct,
                "profit_percent": profit_pct,
                "glass_rate_used": glass_override if glass_override > 0 else self.prices.get('glass', 0)
            }
        }