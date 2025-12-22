# Products package initialization
# This package contains all product type implementations

from .window import WindowProduct
from .door import DoorProduct

# List of all available products
__all__ = ['WindowProduct', 'DoorProduct']
