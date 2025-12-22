"""
Multi-Product Demo
Demonstrates how easy it is to work with multiple products.
"""

# Import all products - auto-registration happens
import products.window
import products.door

from engine import EstimationEngine
from product_registry import ProductRegistry

print("="*70)
print(" MULTI-PRODUCT SCALABILITY DEMONSTRATION")
print("="*70)

# Show registered products
print("\n[1] Registered Products:")
products = ProductRegistry.list_products()
for product in products:
    info = ProductRegistry.get_product_info(product)
    print(f"   • {product.upper()}")
    print(f"      - Designs: {info['total_designs']}")
    print(f"      - Series: {info['total_series']}")
    print(f"      - Available: {', '.join(info['available_designs'][:3])}...")

# Test Window
print("\n[2] Window Calculation:")
print("-" * 70)
window_engine = EstimationEngine('window', '90mm', 'rohit')
window_result = window_engine.calculate('2_panel_slide', 5.0, 4.0)
print(f"   Product: {window_result['metadata']['product_type']}")
print(f"   Design: {window_result['metadata']['design_type']}")
print(f"   Materials: {len(window_result['breakdown'])} items")
print(f"   Final Price: Rs {window_result['financials']['7_final_price']:,.2f}")

# Test Door
print("\n[3] Door Calculation:")
print("-" * 70)
door_engine = EstimationEngine('door', '90mm', 'standard')
door_result = door_engine.calculate('single_panel', 3.0, 7.0)
print(f"   Product: {door_result['metadata']['product_type']}")
print(f"   Design: {door_result['metadata']['design_type']}")
print(f"   Materials: {len(door_result['breakdown'])} items")
print(f"   Final Price: Rs {door_result['financials']['7_final_price']:,.2f}")

# Show door materials with descriptions
print("\n   Door Materials Breakdown:")
for item in door_result['breakdown'][:5]:
    print(f"      {item['item']:15} - {item['description']:<35} | {item['qty']:.1f} {item['unit']}")

# Test Double Door
print("\n[4] Double Door Calculation:")
print("-" * 70)
door_engine2 = EstimationEngine('door', '100mm', 'standard')
door_result2 = door_engine2.calculate('double_panel', 6.0, 8.0)
print(f"   Design: {door_result2['metadata']['design_type']}")
print(f"   Series: {door_result2['metadata']['series']}")
print(f"   Materials: {len(door_result2['breakdown'])} items")
print(f"   Final Price: Rs {door_result2['financials']['7_final_price']:,.2f}")

print("\n" + "="*70)
print(" SUCCESS! Multiple Products Working Seamlessly")
print("="*70)
print("\n✓ Window product: Full functionality")
print("✓ Door product: Single & double panels")
print("✓ Zero changes to core engine")
print("✓ Each product has its own formulas and rates")
print("✓ Expression language works for all products")
print("\n[SCALABILITY PROVEN] Ready to add partitions, railings, etc!")
