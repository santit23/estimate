"""
Estimation Engine Module
Product-agnostic calculation engine that works with any registered product type.
"""

from typing import Optional, Dict
from product_registry import ProductRegistry
from formula_manager import FormulaManager


class EstimationEngine:
    """Main calculation engine for material estimation"""
    
    def __init__(self, product_type: str, series: str, quality: str, 
                 tenant_id: Optional[str] = None, formula_manager: Optional[FormulaManager] = None,
                 custom_prices: Optional[Dict[str, float]] = None,
                 custom_units: Optional[Dict[str, str]] = None):
        """Initialize the estimation engine
        
        Args:
            product_type: Type of product ('window', 'door', etc.)
            series: Series identifier (e.g., '90mm', '78mm')
            quality: Quality/brand identifier (e.g., 'rohit', 'mount')
            tenant_id: Optional tenant ID for multi-tenant support
            formula_manager: Optional custom formula manager instance
            custom_prices: Optional dictionary of {material: price} to override default rates
            custom_units: Optional dictionary of {material: unit} to override default units
        """
        self.product_type = product_type
        self.series = series
        self.quality = quality
        self.tenant_id = tenant_id
        
        # Load product implementation
        self.product = ProductRegistry.get_product(product_type)
        
        # Initialize formula manager
        self.formula_manager = formula_manager or FormulaManager()
        
        # Load rates from product
        rates_data = self.product.get_rates()
        try:
            data = rates_data[series][quality]
            self.rate_config = data['config'].copy()  # {'profile_unit': '20ft', ...}
            self.prices = data['rates'].copy()         # {'topfr': 1200, ...}
            
            # 1. Update prices with custom overrides
            if custom_prices:
                for mat, price in custom_prices.items():
                    self.prices[mat] = price
            
            # 2. Update units with custom overrides
            # Since config.py uses category-based units (profile_unit, etc.), 
            # we allow direct per-material unit overrides if custom_units is provided.
            self.material_unit_overrides = custom_units or {}
            
        except KeyError:
            raise ValueError(f"No data found for {product_type} {series} {quality}")
        
        # Get item categories
        self.item_categories = self.product.get_item_categories()
    
    def calculate(self, design_type: str, width_ft: float, height_ft: float, 
                  quantity: int = 1, has_mesh: bool = False, 
                  variable_inputs: Optional[dict] = None) -> dict:
        """Calculate material quantities and costs for a design
        
        Args:
            design_type: Design identifier (e.g., '2_panel_slide')
            width_ft: Width in feet
            height_ft: Height in feet
            quantity: Number of units
            has_mesh: Whether to include mesh/jali calculations
            variable_inputs: Optional overrides for labour, transport, profit
            
        Returns:
            Dictionary with breakdown and financials
        """
        vars = variable_inputs or {}
        labour_rate = vars.get('labour_rate_sqft', 0.0)
        transport_cost = vars.get('transport_cost', 0.0)
        profit_pct = vars.get('profit_percent', 0.0)
        glass_override = vars.get('glass_price', 0.0)
        
        # Validate design type
        if not self.product.validate_design(design_type):
            available = ', '.join(self.product.get_available_designs())
            raise ValueError(
                f"Unknown design type '{design_type}' for product '{self.product_type}'. "
                f"Available: {available}"
            )
        
        # Get formula configurations from product
        formula_configs = self.product.get_formulas()[design_type]
        
        material_breakdown = []
        net_material_cost = 0
        total_sqft = width_ft * height_ft * quantity
        
        # Calculate each material
        for material, config in formula_configs.items():
            # Skip jali if not requested
            if "jali" in material and not has_mesh:
                continue
            # Skip labour (calculated separately)
            if material == 'labour':
                continue
            
            # Get active formula (custom or default)
            try:
                formula_func = self.formula_manager.get_active_formula(
                    self.product_type, design_type, material, self.tenant_id
                )
            except Exception as e:
                print(f"Warning: Error getting formula for {material}: {e}")
                continue
            
            # Get category (e.g., 'profile', 'hardware')
            category = self.item_categories.get(material, 'other')
            
            # Get unit setting for this material
            # First check if there's a specific override for this material
            if material in self.material_unit_overrides:
                unit_type = self.material_unit_overrides[material]
            else:
                config_key = f"{category}_unit"
                unit_type = self.rate_config.get(config_key, 'nos')  # Default to nos
            
            # Get price
            raw_price = self.prices.get(material, 0)
            
            # Apply Glass Override if applicable
            if material == 'glass' and glass_override > 0:
                raw_price = glass_override
            
            if raw_price == 0:
                continue
            
            # Math conversion logic
            effective_rate = raw_price
            if unit_type == '20ft':
                effective_rate = raw_price / 20.0
            elif unit_type == '12ft':
                effective_rate = raw_price / 12.0
            # 'ft', 'sqft', 'nos' need no divisor
            
            # Calculate quantity required
            try:
                qty_required = formula_func(width_ft, height_ft) * quantity
                cost = qty_required * effective_rate
                
                material_breakdown.append({
                    "item": material,
                    "description": config.get('description', ''),
                    "qty": round(qty_required, 2),
                    "unit": unit_type,
                    "rate": round(raw_price, 2),
                    "amount": round(cost, 2)
                })
                net_material_cost += cost
            except Exception as e:
                print(f"Warning: Error calculating {material}: {e}")
                continue
        
        # --- FINANCIALS ---
        if labour_rate == 0.0:
            labour_rate = self.prices.get('labour', 0)
        
        labour_cost = total_sqft * labour_rate
        production_cost = net_material_cost + labour_cost
        cost_with_transport = production_cost + transport_cost
        profit_amount = cost_with_transport * (profit_pct / 100)
        final_price = cost_with_transport + profit_amount
        
        return {
            "breakdown": material_breakdown,
            "financials": {
                "1_net_material": round(net_material_cost, 2),
                "3_labour_cost": round(labour_cost, 2),
                "4_transport": round(transport_cost, 2),
                "5_total_cost": round(cost_with_transport, 2),
                "6_profit_amt": round(profit_amount, 2),
                "7_final_price": round(final_price, 2)
            },
            "inputs": {
                "profit_percent": profit_pct,
                "glass_rate_used": glass_override if glass_override > 0 else self.prices.get('glass', 0)
            },
            "metadata": {
                "product_type": self.product_type,
                "design_type": design_type,
                "series": self.series,
                "quality": self.quality,
                "dimensions": f"{width_ft}ft x {height_ft}ft",
                "quantity": quantity,
                "has_mesh": has_mesh
            }
        }
    
    def get_available_designs(self):
        """Get list of available designs for current product"""
        return self.product.get_available_designs()
    
    def get_formulas_for_display(self, design_type: str):
        """Get formulas for UI display"""
        return self.formula_manager.get_formulas_for_display(
            self.product_type, design_type, self.tenant_id
        )