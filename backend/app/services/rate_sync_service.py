"""
Rate Sync Service
Synchronizes static JSON rates from config_rates.py to the database.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import MaterialRate
from config import MATERIAL_RATES

def guess_category(name: str) -> str:
    """Helper to guess category based on material name"""
    name = name.lower()
    if any(x in name for x in ['gasket', 'brush', 'guide', 'pile', 'lock', 'handle', 'roller', 'bearing', 'angle']):
        return 'hardware'
    if any(x in name for x in ['fr', 'sht', 'track', 'interlock', 'clip', '11b', '13d', '13', '18', 'profile', 'jali']):
        return 'profile'
    if any(x in name for x in ['glass', 'labour', 'silicon', 'screw']):
        return 'other'
    return 'hardware'

def sync_defaults_to_db(user_id: int, db: Session, series: Optional[str] = None, quality: Optional[str] = None):
    """
    Sync default rates from config_rates.py to user's database.
    Does not overwrite existing rates unless explicitly deleted first.
    """
    sync_count = 0
    
    series_to_sync = [series] if series else MATERIAL_RATES.keys()
    
    for s_id in series_to_sync:
        if s_id not in MATERIAL_RATES: continue
        
        qualities_to_sync = [quality] if quality else MATERIAL_RATES[s_id].keys()
        
        for q_id in qualities_to_sync:
            if q_id not in MATERIAL_RATES[s_id]: continue
            
            data = MATERIAL_RATES[s_id][q_id]
            rates = data.get('rates', {})
            config = data.get('config', {})
            
            # Default colors to initialize
            default_colors = ["mill", "black", "wood", "champagne", "grey", "white"]
            
            for color in default_colors:
                for mat_name, rate in rates.items():
                    # Check if already exists
                    existing = db.query(MaterialRate).filter(
                        MaterialRate.user_id == user_id,
                        MaterialRate.series == s_id,
                        MaterialRate.quality == q_id,
                        MaterialRate.color == color,
                        MaterialRate.material_name == mat_name
                    ).first()
                    
                    if not existing:
                        cat = guess_category(mat_name)
                        
                        # Determine unit
                        unit = 'nos'
                        if cat == 'profile':
                            unit = config.get('profile_unit', '20ft')
                        elif cat == 'hardware':
                            unit = config.get('hardware_unit', 'nos')
                            if mat_name in ['gasket', 'brush', 'red_brush', 'guide', 'jali_gasket', 'wool_pile', 'jali_angle']:
                                unit = config.get('linear_unit', 'ft')
                        elif mat_name == 'glass' or mat_name == 'labour':
                            unit = config.get('area_unit', 'sqft')
                        elif mat_name == 'screw' or mat_name == 'silicon':
                            unit = config.get('consumable_unit', 'set')
                        
                        new_rate = MaterialRate(
                            user_id=user_id,
                            series=s_id,
                            quality=q_id,
                            color=color,
                            material_name=mat_name,
                            rate=rate,
                            unit=unit,
                            category=cat
                        )
                        db.add(new_rate)
                        sync_count += 1
    
    db.commit()
    return sync_count
