"""
Product Registry Module
Centralized registry for managing product type implementations.
"""

from typing import Dict, Type, List
from base_product import BaseProduct


class ProductRegistry:
    """Singleton registry for managing product implementations"""
    
    _products: Dict[str, Type[BaseProduct]] = {}
    _instances: Dict[str, BaseProduct] = {}  # Cache product instances
    
    @classmethod
    def register(cls, product_class: Type[BaseProduct]):
        """Register a product implementation
        
        Args:
            product_class: Class inheriting from BaseProduct
            
        Example:
            ProductRegistry.register(WindowProduct)
        """
        # Create temporary instance to get product name
        temp_instance = product_class()
        product_name = temp_instance.product_name
        
        cls._products[product_name] = product_class
        print(f"[ProductRegistry] Registered product: '{product_name}'")
    
    @classmethod
    def get_product(cls, product_type: str) -> BaseProduct:
        """Retrieve a product implementation instance
        
        Args:
            product_type: Product type identifier (e.g., 'window', 'door')
            
        Returns:
            Product instance
            
        Raises:
            ValueError: If product type is not registered
        """
        if product_type not in cls._products:
            available = ', '.join(cls._products.keys()) if cls._products else 'none'
            raise ValueError(
                f"Unknown product type: '{product_type}'. "
                f"Available products: {available}"
            )
        
        # Return cached instance if exists
        if product_type in cls._instances:
            return cls._instances[product_type]
        
        # Create and cache new instance
        product_class = cls._products[product_type]
        instance = product_class()
        cls._instances[product_type] = instance
        
        return instance
    
    @classmethod
    def list_products(cls) -> List[str]:
        """List all registered product types
        
        Returns:
            List of product type identifiers
        """
        return list(cls._products.keys())
    
    @classmethod
    def is_registered(cls, product_type: str) -> bool:
        """Check if a product type is registered
        
        Args:
            product_type: Product type identifier
            
        Returns:
            True if registered, False otherwise
        """
        return product_type in cls._products
    
    @classmethod
    def clear(cls):
        """Clear all registered products (mainly for testing)"""
        cls._products.clear()
        cls._instances.clear()
    
    @classmethod
    def get_product_info(cls, product_type: str) -> Dict:
        """Get detailed information about a registered product
        
        Args:
            product_type: Product type identifier
            
        Returns:
            Dictionary with product information
        """
        if product_type not in cls._products:
            raise ValueError(f"Unknown product type: '{product_type}'")
        
        product = cls.get_product(product_type)
        
        return {
            'product_name': product.product_name,
            'available_designs': product.get_available_designs(),
            'available_series': product.get_available_series(),
            'total_designs': len(product.get_available_designs()),
            'total_series': len(product.get_available_series())
        }
