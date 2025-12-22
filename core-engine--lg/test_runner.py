# test_runner.py
import sys
from engine import EstimationEngine

def get_input(prompt, default=None, type_func=str):
    """Helper to get user input with default values"""
    user_val = input(f"{prompt} (Default: {default}): ") if default else input(f"{prompt}: ")
    
    if not user_val and default is not None:
        return default
    
    try:
        return type_func(user_val)
    except ValueError:
        print(f"Invalid input. Using default {default}")
        return default

def run_interactive():
    print("\n" + "="*50)
    print("      ALUMINIUM ESTIMATION SYSTEM (TERMINAL)      ")
    print("="*50)

    # ==========================================
    # 1. PROJECT CONFIGURATION (Fixed Logic)
    # ==========================================
    print("\n--- [1] WINDOW DETAILS ---")
    
    # In a real app, these would be dropdowns
    series = get_input("   Series (e.g. 90mm, 78mm)", "90mm")
    brand = get_input("   Brand (e.g. rohit, mount)", "rohit")
    
    design = get_input("   Design Type (e.g. 2_panel_slide, 3_panel_slide)", "2_panel_slide")
    
    width = get_input("   Width (ft)", 0.0, float)
    height = get_input("   Height (ft)", 0.0, float)
    qty = get_input("   Quantity", 1, int)
    
    mesh_input = get_input("   Include Mesh/Jali? (y/n)", "n").lower()
    has_mesh = True if mesh_input == 'y' else False

    # ==========================================
    # 2. COSTING VARIABLES (Job Specific)
    # ==========================================
    print("\n--- [2] VARIABLE COSTS (OVERHEADS) ---")

    glass_in = input("   Glass Rate per SqFt (Press Enter for Default): ")
    glass_val = float(glass_in) if glass_in.strip() else 0.0

    
    # Labour: Optional Override
    labour_input = input("   Labour Rate per SqFt (Press Enter to use Database Rate): ")
    labour_override = float(labour_input) if labour_input.strip() else None

    # wastage_pct = get_input("   Wastage Percentage", 5.0, float)
    transport = get_input("   Transport/Cartage Cost (Rs)", 0.0, float)
    profit_pct = get_input("   Profit Margin %", 20.0, float)

    # Pack variables for the engine
    variable_inputs = {
        # 'wastage_percent': wastage_pct,
        'transport_cost': transport,
        'profit_percent': profit_pct
    }
    if labour_override is not None:
        variable_inputs['labour_rate_sqft'] = labour_override

    # ==========================================
    # 3. EXECUTION
    # ==========================================
    try:
        engine = EstimationEngine(series, brand)
        result = engine.calculate(
            design_type=design, 
            width_ft=width, 
            height_ft=height, 
            quantity=qty, 
            has_mesh=has_mesh, 
            variable_inputs=variable_inputs
        )
    except ValueError as e:
        print(f"\n[ERROR] Calculation Failed: {e}")
        return

    # ==========================================
    # 4. OUTPUT / QUOTATION
    # ==========================================
    fin = result['financials']
    inputs = result['inputs']
    
    print("\n\n")
    print("="*60)
    print(f"QUOTATION SUMMARY | {brand.upper()} {series} | {design.replace('_', ' ').title()}")
    print(f"Size: {width}x{height} ft | Qty: {qty} | Mesh: {'YES' if has_mesh else 'NO'}")
    print("="*60)

    # A. Material Table
    print(f"{'ITEM':<20} | {'QTY':<8} | {'UNIT':<6} | {'RATE':<8} | {'AMOUNT':<10}")
    print("-" * 65)
    
    for item in result['breakdown']:
        print(f"{item['item']:<20} | {item['qty']:<8} | {item['unit']:<6} | {item['rate']:<8} | {item['amount']:<10}")
    
    print("-" * 65)
    
    # B. Financial Breakdown
    # FIX: We use double quotes "..." for the f-string so we can use single quotes '...' inside
    print(f"{'A. Net Material Cost':<45} : Rs {fin['1_net_material']:>10}")
    
    # wastage_label = f"B. Wastage ({inputs['wastage_percent']}%)"
    # print(f"{wastage_label:<45} : Rs {fin['2_wastage_amt']:>10}")
    
    print(f"{'C. Labour Charges':<45} : Rs {fin['3_labour_cost']:>10}")
    print(f"{'D. Transport/Cartage':<45} : Rs {fin['4_transport']:>10}")
    print("-" * 60)
    print(f"{'PRODUCTION COST (A+B+C+D)':<45} : Rs {fin['5_total_cost']:>10}")
    
    profit_label = f"PROFIT MARGIN ({inputs['profit_percent']}%)"
    print(f"{profit_label:<45} : Rs {fin['6_profit_amt']:>10}")
    
    print("=" * 60)
    print(f"{'FINAL QUOTATION PRICE':<45} : Rs {fin['7_final_price']:>10}")
    print("=" * 60)

if __name__ == "__main__":
    run_interactive()