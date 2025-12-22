from sqlalchemy.orm import Session
from app.services import core_engine_service

def calculate_estimate_for_item(item_data, user_id: int, db: Session, variable_inputs: dict = None):
    """
    Calculate estimate using the core-engine service.
    Acts as a bridge between the API and the core-engine.
    """
    # Call the new core engine
    result = core_engine_service.calculate_estimate_with_core_engine(
        product_type="window", # Defaulting to window for now
        design=item_data.design,
        series=item_data.series,
        quality=item_data.quality,
        width=item_data.width,
        height=item_data.height,
        quantity=item_data.quantity,
        user_id=user_id,
        db=db,
        color=item_data.color,
        variable_inputs=variable_inputs
    )
    
    # Map core-engine result to expected format for API
    # Core engine returns { "financials": { "total_cost": ... }, ... }
    # API expects { "total_cost": ... }
    
    return {
        "total": result['financials']['5_total_cost'], # For compatibility with update_estimate
        "total_cost": result['financials']['5_total_cost'], # For compatibility with create_estimate
        "breakdown": result['breakdown'],
        "metadata": result['metadata']
    }

