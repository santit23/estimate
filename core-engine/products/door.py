"""
Door Product Implementation
Example showing how easy it is to add a new product type.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_product import BaseProduct


class DoorProduct(BaseProduct):
    """Door estimation product implementation"""
    
    @property
    def product_name(self) -> str:
        return "door"
    
    def get_formulas(self):
        """Door-specific formulas"""
        return {
            "single_panel": {
                'topfr': {
                    'expression': 'l',
                    'description': 'Top frame for single door',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'bottomfr': {
                    'expression': 'l',
                    'description': 'Bottom frame',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'sidefr': {
                    'expression': 'h * 2',
                    'description': 'Side frames (both sides)',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'door_shutter': {
                    'expression': 'l * 2 + h * 2',
                    'description': 'Door shutter perimeter',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'glass': {
                    'expression': 'l * h * 0.8',
                    'description': 'Glass area (80% for door panel)',
                    'unit': 'sqft',
                    'constraints': {'min': 0}
                },
                'hinges': {
                    'expression': 'if(h > 7, 4, 3)',
                    'description': 'More hinges for taller doors',
                    'unit': 'nos',
                    'constraints': {'min': 2, 'max': 6}
                },
                'handle': {
                    'expression': '1',
                    'description': 'Door handle set',
                    'unit': 'set',
                    'constraints': {'min': 1}
                },
                'lock': {
                    'expression': '1',
                    'description': 'Door lock',
                    'unit': 'nos',
                    'constraints': {'min': 1}
                },
                'gasket': {
                    'expression': '(l * 2) + (h * 2)',
                    'description': 'Gasket perimeter',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'labour': {
                    'expression': 'l * h',
                    'description': 'Labour cost based on area',
                    'unit': 'sqft',
                    'constraints': {'min': 0}
                },
            },
            
            "double_panel": {
                'topfr': {
                    'expression': 'l',
                    'description': 'Top frame full width',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'bottomfr': {
                    'expression': 'l',
                    'description': 'Bottom frame',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'sidefr': {
                    'expression': 'h * 2',
                    'description': 'Side frames',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'center_mullion': {
                    'expression': 'h',
                    'description': 'Center divider',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'door_shutter': {
                    'expression': '(l * 2) + (h * 4)',
                    'description': 'Both door shutters',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'glass': {
                    'expression': 'l * h * 0.75',
                    'description': 'Glass for both panels',
                    'unit': 'sqft',
                    'constraints': {'min': 0}
                },
                'hinges': {
                    'expression': 'if(h > 7, 8, 6)',
                    'description': 'Hinges for both doors',
                    'unit': 'nos',
                    'constraints': {'min': 4, 'max': 12}
                },
                'handle': {
                    'expression': '2',
                    'description': 'Handle sets (both doors)',
                    'unit': 'set',
                    'constraints': {'min': 2}
                },
                'lock': {
                    'expression': '1',
                    'description': 'Main lock',
                    'unit': 'nos',
                    'constraints': {'min': 1}
                },
                'gasket': {
                    'expression': '(l * 2) + (h * 4)',
                    'description': 'Gasket for both panels',
                    'unit': 'ft',
                    'constraints': {'min': 0}
                },
                'labour': {
                    'expression': 'l * h',
                    'description': 'Labour cost',
                    'unit': 'sqft',
                    'constraints': {'min': 0}
                },
            }
        }
    
    def get_rates(self):
        """Door-specific material rates"""
        return {
            '90mm': {
                'standard': {
                    'config': {
                        'profile_unit': 'ft',
                        'linear_unit': 'ft',
                        'area_unit': 'sqft',
                        'hardware_unit': 'nos',
                        'consumable_unit': 'set'
                    },
                    'rates': {
                        'topfr': 8,
                        'bottomfr': 8,
                        'sidefr': 10,
                        'center_mullion': 10,
                        'door_shutter': 12,
                        'glass': 25,
                        'hinges': 50,
                        'handle': 200,
                        'lock': 300,
                        'gasket': 15,
                        'labour': 15,
                    }
                },
                'premium': {
                    'config': {
                        'profile_unit': 'ft',
                        'linear_unit': 'ft',
                        'area_unit': 'sqft',
                        'hardware_unit': 'nos',
                        'consumable_unit': 'set'
                    },
                    'rates': {
                        'topfr': 12,
                        'bottomfr': 12,
                        'sidefr': 15,
                        'center_mullion': 15,
                        'door_shutter': 18,
                        'glass': 35,
                        'hinges': 80,
                        'handle': 350,
                        'lock': 500,
                        'gasket': 20,
                        'labour': 20,
                    }
                }
            },
            '100mm': {
                'standard': {
                    'config': {
                        'profile_unit': 'ft',
                        'linear_unit': 'ft',
                        'area_unit': 'sqft',
                        'hardware_unit': 'nos',
                        'consumable_unit': 'set'
                    },
                    'rates': {
                        'topfr': 10,
                        'bottomfr': 10,
                        'sidefr': 12,
                        'center_mullion': 12,
                        'door_shutter': 14,
                        'glass': 30,
                        'hinges': 60,
                        'handle': 250,
                        'lock': 400,
                        'gasket': 18,
                        'labour': 18,
                    }
                }
            }
        }
    
    def get_item_categories(self):
        """Door material category mappings"""
        return {
            'topfr': 'profile',
            'bottomfr': 'profile',
            'sidefr': 'profile',
            'center_mullion': 'profile',
            'door_shutter': 'profile',
            'glass': 'area',
            'gasket': 'linear',
            'hinges': 'hardware',
            'handle': 'hardware',
            'lock': 'hardware',
            'labour': 'area',
        }


# Auto-register this product when module is imported
if __name__ != "__main__":
    from product_registry import ProductRegistry
    ProductRegistry.register(DoorProduct)
