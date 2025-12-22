"""
Core Engine Service
Integrates the new core-engine for material estimation and formula management.
"""

import sys
import os
from typing import Dict, Optional
from sqlalchemy.orm import Session

# Add core-engine to path - go up from app/services to backend, then to estimate, then to core-engine
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
estimate_dir = os.path.dirname(backend_dir)
core_engine_path = os.path.join(estimate_dir, 'core-engine')

if core_engine_path not in sys.path:
    sys.path.insert(0, core_engine_path)

from engine import EstimationEngine
from formula_manager import FormulaManager
from app.models.models import MaterialRate
# Import products to register them
import products.window


# Global formula manager instance for session-based formula customization
_formula_manager = FormulaManager()


def get_user_rates_for_core_engine(user_id: int, db: Session, series: str, quality: str, color: Optional[str] = None):
    """
    Fetch user's material rates for specific series/quality/color.
    Returns (price_map, unit_map) or (None, None) if no custom rates found.
    """
    query = db.query(MaterialRate).filter(
        MaterialRate.user_id == user_id,
        MaterialRate.series == series,
        MaterialRate.quality == quality
    )
    
    if color:
        query = query.filter(MaterialRate.color == color)
    else:
        query = query.filter(MaterialRate.color == "mill")
        
    rates = query.all()
    
    if not rates:
        return None, None
        
    price_map = {}
    unit_map = {}
    for r in rates:
        price_map[r.material_name] = r.rate
        if r.unit:
            unit_map[r.material_name] = r.unit
        
    return price_map, unit_map


def design_type_mapper(frontend_design: str) -> str:
    """
    Map frontend design names to core-engine design types.
    
    Args:
        frontend_design: Design name from frontend (e.g., '2panel', '3panel')
    
    Returns:
        Core-engine design type (e.g., '2_panel_slide', '3_panel_slide')
    """
    mapping = {
        '2panel': '2_panel_slide',
        '3panel': '3_panel_slide',
        '4panel': '4_panel_slide',
        '2panel_topfix': '2_pnl_topfix',
        '3panel_topfix': '3_pnl_topfix',
        '4panel_topfix': '4_pnl_topfix',
    }
    
    return mapping.get(frontend_design, frontend_design)


def reverse_design_mapper(core_engine_design: str) -> str:
    """Map core-engine design type back to frontend design name"""
    reverse_mapping = {
        '2_panel_slide': '2panel',
        '3_panel_slide': '3panel',
        '4_panel_slide': '4panel',
        '2_pnl_topfix': '2panel_topfix',
        '3_pnl_topfix': '3panel_topfix',
        '4_pnl_topfix': '4panel_topfix',
    }
    
    return reverse_mapping.get(core_engine_design, core_engine_design)


def calculate_estimate_with_core_engine(
    product_type: str,
    design: str,
    series: str,
    quality: str,
    width: float,
    height: float,
    quantity: int,
    user_id: int,
    db: Session,
    has_mesh: bool = False,
    variable_inputs: Optional[Dict] = None,
    color: Optional[str] = None
) -> Dict:
    """
    Calculate estimate using the new core-engine.
    
    Args:
        product_type: Product type (e.g., 'window', 'door')
        design: Design type from frontend
        series: Series identifier (e.g., '90mm', '78mm')
        quality: Quality/brand (e.g., 'mount', 'rohit')
        width: Width in feet
        height: Height in feet
        quantity: Number of units
        user_id: User ID for fetching rates
        db: Database session
        has_mesh: Whether to include mesh calculations
        variable_inputs: Optional overrides for labour, transport, profit
    
    Returns:
        Calculation result from core-engine with breakdown and financials
    """
    # Map design to core-engine format
    core_design = design_type_mapper(design)
    
    # Get user rates in core-engine format
    # Note: Core-engine loads rates from product.get_rates() by default
    # For user-specific rates, we need to inject them
    # For now, we'll use the default rates from core-engine
    # TODO: Implement custom rates injection if needed
    
    # Get user rates
    custom_prices, custom_units = get_user_rates_for_core_engine(user_id, db, series, quality, color)
    
    try:
        # Initialize engine with formula manager AND custom prices/units
        engine = EstimationEngine(
            product_type=product_type,
            series=series,
            quality=quality,
            tenant_id=str(user_id),
            formula_manager=_formula_manager,
            custom_prices=custom_prices,
            custom_units=custom_units
        )
        
        # Calculate
        result = engine.calculate(
            design_type=core_design,
            width_ft=width,
            height_ft=height,
            quantity=quantity,
            has_mesh=has_mesh,
            variable_inputs=variable_inputs or {}
        )
        
        return result
        
    except ValueError as e:
        raise ValueError(f"Calculation error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error in core-engine: {str(e)}")


def get_formulas_for_display(
    product_type: str,
    design: str,
    tenant_id: Optional[str] = None
) -> Dict:
    """
    Get all formulas for a design type in UI-friendly format.
    
    Args:
        product_type: Product type (e.g., 'window', 'door')
        design: Design type from frontend
        tenant_id: Optional tenant ID for custom formulas
    
    Returns:
        Dictionary of formulas with metadata
    """
    core_design = design_type_mapper(design)
    
    try:
        formulas = _formula_manager.get_formulas_for_display(
            product_type=product_type,
            design_type=core_design,
            tenant_id=tenant_id
        )
        return formulas
    except Exception as e:
        raise ValueError(f"Error getting formulas: {str(e)}")


def update_formula(
    product_type: str,
    design: str,
    material: str,
    expression: str,
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> bool:
    """
    Update a formula expression.
    
    Returns:
        True if successful
    """
    core_design = design_type_mapper(design)
    
    try:
        _formula_manager.update_formula(
            product_type=product_type,
            design_type=core_design,
            material=material,
            expression=expression,
            tenant_id=tenant_id,
            user_id=user_id
        )
        return True
    except Exception as e:
        raise ValueError(f"Error updating formula: {str(e)}")


def reset_formula(
    product_type: str,
    design: str,
    material: str,
    tenant_id: Optional[str] = None
) -> bool:
    """
    Reset a formula to its default value.
    
    Returns:
        True if successful
    """
    core_design = design_type_mapper(design)
    
    try:
        _formula_manager.reset_formula(
            product_type=product_type,
            design_type=core_design,
            material=material,
            tenant_id=tenant_id
        )
        return True
    except Exception as e:
        raise ValueError(f"Error resetting formula: {str(e)}")


def validate_formula(expression: str) -> Dict:
    """
    Validate a formula expression.
    
    Returns:
        {
            'valid': bool,
            'error': str or None,
            'test_result': float or None
        }
    """
    try:
        result = _formula_manager.validate_formula(expression)
        return result
    except Exception as e:
        return {
            'valid': False,
            'error': str(e),
            'test_result': None
        }
