from sqlalchemy.orm import Session
from app.models.models import MaterialRate
from estimator import get_estimator_by_design

def get_user_rates(user_id: int, db: Session):
    """
    Fetches material rates for a specific user and reconstructs the nested dictionary
    format required by the legacy estimator logic.
    """
    rates = db.query(MaterialRate).filter(MaterialRate.user_id == user_id).all()
    
    # Reconstruct nested dict: rates_config[series][quality][material]
    rates_config = {}
    
    for r in rates:
        if r.series not in rates_config:
            rates_config[r.series] = {}
        if r.quality not in rates_config[r.series]:
            rates_config[r.series][r.quality] = {}
        
        rates_config[r.series][r.quality][r.material_name] = r.rate
        
    return rates_config

def calculate_estimate_for_item(item_data, user_id: int, db: Session):
    rates_config = get_user_rates(user_id, db)
    
    # Check if series/quality exists in user rates, if not fallback or error
    # For now, we assume the user has rates for what they select
    
    estimator = get_estimator_by_design(item_data.design, rates_config)
    result = estimator.estimate(
        item_data.series, 
        item_data.quality, 
        item_data.width, 
        item_data.height, 
        item_data.quantity
    )
    return result
