"""
Window Product Implementation
Implements the BaseProduct interface for window estimations.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_product import BaseProduct
from config_formulas import WINDOW_FORMULAS
from config_rates import MATERIAL_RATES
from config_categories import ITEM_CATEGORY_MAP


class WindowProduct(BaseProduct):
    """Window estimation product implementation"""
    
    @property
    def product_name(self) -> str:
        return "window"
    
    def get_formulas(self):
        """Get all window formula configurations"""
        return WINDOW_FORMULAS
    
    def get_rates(self):
        """Get all window material rates"""
        return MATERIAL_RATES
    
    def get_item_categories(self):
        """Get material category mappings for windows"""
        return ITEM_CATEGORY_MAP


# Auto-register this product when module is imported
if __name__ != "__main__":
    from product_registry import ProductRegistry
    ProductRegistry.register(WindowProduct)
