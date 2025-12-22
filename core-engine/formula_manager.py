"""
Formula Manager Module
Handles formula evaluation, validation, and customization for the estimation engine.
Supports expression language with built-in functions.
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime
import math

try:
    from simpleeval import simple_eval, NameNotDefined, FunctionNotDefined
    HAS_SIMPLEEVAL = True
except ImportError:
    HAS_SIMPLEEVAL = False
    print("WARNING: simpleeval not installed. Install with: pip install simpleeval")
    print("Falling back to basic eval (less secure)")


class FormulaManager:
    """Manages formula viewing, editing, and validation with expression language support"""
    
    # Built-in functions available to all formulas
    BUILTIN_FUNCTIONS = {
        'max': max,
        'min': min,
        'round': round,
        'ceiling': math.ceil,
        'floor': math.floor,
        'abs': abs,
        'if': lambda cond, true_val, false_val: true_val if cond else false_val,
    }
    
    def __init__(self):
        self.custom_formulas = {}  # Stores tenant-specific overrides
    
    def evaluate_expression(self, expression: str, length: float, height: float) -> float:
        """Evaluate a formula expression with given dimensions
        
        Args:
            expression: Formula string like "l * 2" or "max(l, h)"
            length: Length/width value
            height: Height value
            
        Returns:
            Calculated result as float
            
        Example:
            >>> manager = FormulaManager()
            >>> manager.evaluate_expression("l * 2", 5.0, 4.0)
            10.0
            >>> manager.evaluate_expression("if(l > 5, l * 1.5, l)", 6.0, 4.0)
            9.0
        """
        try:
            if HAS_SIMPLEEVAL:
                result = simple_eval(
                    expression,
                    names={'l': length, 'h': height},
                    functions=self.BUILTIN_FUNCTIONS
                )
            else:
                # Fallback to basic eval (less secure, but works without dependency)
                # Add builtin functions to local scope
                local_scope = {
                    'l': length,
                    'h': height,
                    **self.BUILTIN_FUNCTIONS
                }
                # Replace 'if' function with lambda (since 'if' is a keyword)
                expr_modified = expression.replace('if(', '__if__(')
                local_scope['__if__'] = self.BUILTIN_FUNCTIONS['if']
                result = eval(expr_modified, {"__builtins__": {}}, local_scope)
            
            return float(result)
        except (NameNotDefined, FunctionNotDefined, NameError, Exception) as e:
            raise ValueError(f"Formula evaluation error: {e}")
    
    def validate_formula(self, expression: str) -> Dict[str, Any]:
        """Validate a formula expression
        
        Returns:
            {
                'valid': bool,
                'error': str or None,
                'test_result': float or None
            }
        """
        try:
            # Test with sample values
            test_result = self.evaluate_expression(expression, 5.0, 4.0)
            
            # Check that result is a number
            if not isinstance(test_result, (int, float)):
                return {
                    'valid': False,
                    'error': f"Formula must return a number, got {type(test_result).__name__}",
                    'test_result': None
                }
            
            # Check for NaN or infinity
            if math.isnan(test_result) or math.isinf(test_result):
                return {
                    'valid': False,
                    'error': "Formula produces invalid result (NaN or Infinity)",
                    'test_result': None
                }
            
            return {
                'valid': True,
                'error': None,
                'test_result': test_result
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'test_result': None
            }
    
    def create_callable(self, expression: str) -> Callable:
        """Convert expression string to callable function
        
        Args:
            expression: Formula string
            
        Returns:
            Lambda function with signature (l, h) -> float
        """
        return lambda l, h: self.evaluate_expression(expression, l, h)
    
    def get_formulas_for_display(self, product_type: str, design_type: str, 
                                 tenant_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Get all formulas for a design in UI-friendly format with metadata
        
        Returns:
            {
                'topfr': {
                    'expression': 'l',
                    'description': 'Top frame length',
                    'unit': 'ft',
                    'is_custom': False,
                    'default_expression': None,
                    'constraints': {'min': 0, 'max': 100}
                },
                ...
            }
        """
        # Import here to avoid circular dependency
        from product_registry import ProductRegistry
        
        product = ProductRegistry.get_product(product_type)
        formulas = product.get_formulas()[design_type]
        
        result = {}
        for material, config in formulas.items():
            # Check if there's a custom override
            custom_key = self._make_key(product_type, design_type, material, tenant_id)
            is_custom = custom_key in self.custom_formulas
            
            if is_custom:
                custom_data = self.custom_formulas[custom_key]
                result[material] = {
                    'expression': custom_data['expression'],
                    'description': config.get('description', ''),
                    'unit': config.get('unit', ''),
                    'is_custom': True,
                    'default_expression': config['expression'],
                    'constraints': config.get('constraints', {}),
                    'updated_at': custom_data.get('updated_at'),
                    'updated_by': custom_data.get('updated_by')
                }
            else:
                result[material] = {
                    'expression': config['expression'],
                    'description': config.get('description', ''),
                    'unit': config.get('unit', ''),
                    'is_custom': False,
                    'default_expression': None,
                    'constraints': config.get('constraints', {})
                }
        
        return result
    
    def update_formula(self, product_type: str, design_type: str, material: str,
                      expression: str, tenant_id: Optional[str] = None, user_id: Optional[str] = None):
        """Update a formula for a specific material
        
        Args:
            product_type: e.g., 'window', 'door'
            design_type: e.g., '2_panel_slide'
            material: e.g., 'topfr'
            expression: Formula string like "l * 2" or "max(l, h)"
            tenant_id: Optional tenant identifier
            user_id: Optional user who made the change
        """
        # Validate the formula
        validation = self.validate_formula(expression)
        if not validation['valid']:
            raise ValueError(f"Invalid formula: {validation['error']}")
        
        # Store the custom formula
        key = self._make_key(product_type, design_type, material, tenant_id)
        
        self.custom_formulas[key] = {
            'expression': expression,
            'function': self.create_callable(expression),
            'updated_at': datetime.now().isoformat(),
            'updated_by': user_id
        }
    
    def reset_formula(self, product_type: str, design_type: str, material: str, 
                     tenant_id: Optional[str] = None):
        """Reset a formula to its default value"""
        key = self._make_key(product_type, design_type, material, tenant_id)
        if key in self.custom_formulas:
            del self.custom_formulas[key]
    
    def get_active_formula(self, product_type: str, design_type: str, material: str,
                          tenant_id: Optional[str] = None) -> Callable:
        """Get the currently active formula function (custom if exists, otherwise default)"""
        key = self._make_key(product_type, design_type, material, tenant_id)
        
        # Check for custom formula
        if key in self.custom_formulas:
            return self.custom_formulas[key]['function']
        
        # Fall back to default
        from product_registry import ProductRegistry
        product = ProductRegistry.get_product(product_type)
        formula_config = product.get_formulas()[design_type][material]
        return self.create_callable(formula_config['expression'])
    
    def export_formulas(self, product_type: str, design_type: str, 
                       tenant_id: Optional[str] = None) -> Dict:
        """Export all formulas (for backup or migration)"""
        formulas = self.get_formulas_for_display(product_type, design_type, tenant_id)
        return {
            'product_type': product_type,
            'design_type': design_type,
            'tenant_id': tenant_id,
            'formulas': formulas,
            'exported_at': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def import_formulas(self, export_data: Dict):
        """Import formulas from export data"""
        for material, data in export_data['formulas'].items():
            if data['is_custom']:
                self.update_formula(
                    export_data['product_type'],
                    export_data['design_type'],
                    material,
                    data['expression'],
                    export_data.get('tenant_id')
                )
    
    def _make_key(self, product_type: str, design_type: str, material: str,
                  tenant_id: Optional[str] = None) -> str:
        """Create a unique key for formula storage"""
        key = f"{product_type}:{design_type}:{material}"
        if tenant_id:
            key = f"{tenant_id}:{key}"
        return key


# Quick usage example
if __name__ == "__main__":
    manager = FormulaManager()
    
    # Test basic evaluation
    print("Testing formula evaluation:")
    print(f"l * 2 with l=5, h=4: {manager.evaluate_expression('l * 2', 5, 4)}")
    print(f"l * h with l=5, h=4: {manager.evaluate_expression('l * h', 5, 4)}")
    print(f"max(l, h) with l=5, h=4: {manager.evaluate_expression('max(l, h)', 5, 4)}")
    print(f"if(l > 6, 6, 4) with l=5, h=4: {manager.evaluate_expression('if(l > 6, 6, 4)', 5, 4)}")
    print(f"if(l > 6, 6, 4) with l=7, h=4: {manager.evaluate_expression('if(l > 6, 6, 4)', 7, 4)}")
    
    # Test validation
    print("\nTesting formula validation:")
    valid = manager.validate_formula('l * 2')
    print(f"'l * 2': {valid}")
    
    invalid = manager.validate_formula('l * x')
    print(f"'l * x': {invalid}")
