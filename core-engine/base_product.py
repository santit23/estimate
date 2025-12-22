"""
Base Product Module
Defines the abstract base class that all product types must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Callable, Any


class BaseProduct(ABC):
    """Abstract base class for all estimatable products (windows, doors, partitions, etc.)"""
    
    @property
    @abstractmethod
    def product_name(self) -> str:
        """Unique identifier for this product type
        
        Returns:
            Product name (e.g., 'window', 'door', 'partition')
        """
        pass
    
    @abstractmethod
    def get_formulas(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Returns design-specific calculation formulas with metadata
        
        Returns:
            Dictionary structure:
            {
                'design_type': {
                    'material': {
                        'expression': str,  # Formula expression like "l * 2"
                        'description': str,  # Human-readable description
                        'unit': str,  # Unit of measurement
                        'constraints': dict  # Min/max constraints
                    },
                    ...
                },
                ...
            }
        
        Example:
            {
                '2_panel_slide': {
                    'topfr': {
                        'expression': 'l',
                        'description': 'Top frame full length',
                        'unit': 'ft',
                        'constraints': {'min': 0}
                    }
                }
            }
        """
        pass
    
    @abstractmethod
    def get_rates(self) -> Dict[str, Dict[str, Any]]:
        """Returns series/quality-specific rates and configuration
        
        Returns:
            Dictionary structure:
            {
                'series': {
                    'quality': {
                        'config': {
                            'profile_unit': str,  # e.g., '20ft', 'ft', 'nos'
                            'linear_unit': str,
                            'area_unit': str,
                            ...
                        },
                        'rates': {
                            'material': float,  # Price per unit
                            ...
                        }
                    }
                }
            }
        """
        pass
    
    @abstractmethod
    def get_item_categories(self) -> Dict[str, str]:
        """Returns material to category mappings
        
        Returns:
            Dictionary mapping material names to categories
            {
                'material_name': 'category',  # e.g., 'topfr': 'profile'
                ...
            }
        
        Categories typically include:
            - 'profile': Aluminium profiles
            - 'linear': Rubber/gasket/brush (per foot)
            - 'area': Glass, mesh (per sqft)
            - 'hardware': Rollers, locks, handles (per piece)
            - 'consumable': Screws, silicon (lump sum)
        """
        pass
    
    def validate_design(self, design_type: str) -> bool:
        """Validates if design type is supported by this product
        
        Args:
            design_type: Design identifier to check
            
        Returns:
            True if design is supported, False otherwise
        """
        return design_type in self.get_formulas()
    
    def get_available_designs(self) -> list:
        """Get list of all available designs for this product
        
        Returns:
            List of design type identifiers
        """
        return list(self.get_formulas().keys())
    
    def get_available_series(self) -> list:
        """Get list of all available series for this product
        
        Returns:
            List of series identifiers
        """
        return list(self.get_rates().keys())
    
    def get_available_qualities(self, series: str) -> list:
        """Get list of available qualities for a specific series
        
        Args:
            series: Series identifier
            
        Returns:
            List of quality/brand identifiers
        """
        rates = self.get_rates()
        if series in rates:
            return list(rates[series].keys())
        return []
