from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.models import User, MaterialRate
from app.schemas.material_rate import MaterialRateResponse, BulkRateUpdate, MaterialRateCreate
from app.services.rate_sync_service import sync_defaults_to_db
from config import MATERIAL_RATES

router = APIRouter()

@router.post("/sync")
def sync_rates(
    series: Optional[str] = None,
    quality: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync default rates to user's database"""
    count = sync_defaults_to_db(current_user.id, db, series, quality)
    return {"message": f"Successfully synced {count} rates"}

@router.get("/", response_model=List[MaterialRateResponse])
def get_rates(
    series: Optional[str] = None,
    quality: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(MaterialRate).filter(MaterialRate.user_id == current_user.id)
    if series:
        query = query.filter(MaterialRate.series == series)
    if quality:
        query = query.filter(MaterialRate.quality == quality)
    
    return query.all()

@router.post("/bulk", response_model=List[MaterialRateResponse])
def bulk_update_rates(
    rate_data: BulkRateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Bulk update or create rates.
    If 'id' is provided and belongs to user, update.
    Otherwise create new.
    Handles 'color' field.
    """
    updated_rates = []
    
    for item in rate_data.rates:
        if item.id:
            # Update existing
            db_rate = db.query(MaterialRate).filter(
                MaterialRate.id == item.id,
                MaterialRate.user_id == current_user.id
            ).first()
            if db_rate:
                db_rate.rate = item.rate
                db_rate.material_name = item.material_name
                db_rate.unit = item.unit
                db_rate.category = item.category
                updated_rates.append(db_rate)
        else:
            # Check if exists by unique combo (series, quality, color, material)
            db_rate = db.query(MaterialRate).filter(
                MaterialRate.user_id == current_user.id,
                MaterialRate.series == item.series,
                MaterialRate.quality == item.quality,
                MaterialRate.color == item.color,
                MaterialRate.material_name == item.material_name
            ).first()
            
            if db_rate:
                db_rate.rate = item.rate
                db_rate.unit = item.unit
                db_rate.category = item.category
                updated_rates.append(db_rate)
            else:
                # Create new
                new_rate = MaterialRate(
                    user_id=current_user.id,
                    series=item.series,
                    quality=item.quality,
                    color=item.color,
                    material_name=item.material_name,
                    rate=item.rate,
                    unit=item.unit,
                    category=item.category
                )
                db.add(new_rate)
                updated_rates.append(new_rate)
    
    db.commit()
    for r in updated_rates:
        db.refresh(r)
        
    return updated_rates

    # ... (existing loop for config materials)

    # MERGE: Fetch materials from DB that might be custom created by user
    # We need to inject `db` dependency into this function signature first!
    # But wait, `get_rate_structure` didn't have `db`. I need to add it.
    pass

@router.delete("/material")
def delete_material(
    material_name: str,
    series: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(MaterialRate).filter(
        MaterialRate.user_id == current_user.id,
        MaterialRate.material_name == material_name
    )
    if series:
        query = query.filter(MaterialRate.series == series)
    
    count = query.delete()
    db.commit()
    return {"deleted": count}

@router.delete("/scope")
def delete_scope_rates(
    series: str,
    quality: Optional[str] = None,
    color: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete rates by scope (e.g. all rates for a specific color/quality/series).
    """
    query = db.query(MaterialRate).filter(
        MaterialRate.user_id == current_user.id,
        MaterialRate.series == series
    )
    if quality:
        query = query.filter(MaterialRate.quality == quality)
    if color:
        query = query.filter(MaterialRate.color == color)
        
    count = query.delete()
    db.commit()
    return {"deleted": count}

@router.get("/structure")
def get_rate_structure(
    series: Optional[str] = None, 
    quality: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Return structure for UI: available series, qualities, materials (with defaults).
    Merges config-defined materials with user-defined materials from DB.
    """
    series_list = list(MATERIAL_RATES.keys())
    qualities = set()
    materials_set = set()
    
    # Helper to guess category
    def guess_category(name):
        name = name.lower()
        # Hardware keywords taking precedence
        if any(x in name for x in ['gasket', 'brush', 'guide', 'pile', 'lock', 'handle', 'roller', 'bearing', 'angle']):
            return 'hardware'
        # Profile keywords
        if any(x in name for x in ['fr', 'sht', 'track', 'interlock', 'clip', '11b', '13d', '13', '18', 'profile', 'jali']):
            return 'profile'
        if any(x in name for x in ['glass', 'labour', 'silicon', 'screw']):
            return 'other'
        return 'hardware'

    # Collect all available materials
    formatted_materials = []
    seen_materials = set()

    for s in series_list:
        for q in MATERIAL_RATES[s].keys():
            qualities.add(q)
            data = MATERIAL_RATES[s][q]
            current_rates = {}
            current_config = {}
            
            if 'rates' in data and 'config' in data:
                 current_rates = data['rates']
                 current_config = data['config']
            else:
                 current_rates = data
                 current_config = {
                     'profile_unit': '20ft', 
                     'hardware_unit': 'nos',
                     'area_unit': 'sqft',
                     'linear_unit': 'ft'
                 }

            for m in current_rates.keys():
                if m not in seen_materials:
                    seen_materials.add(m)
                    cat = guess_category(m)
                    
                    unit = 'nos'
                    if cat == 'profile':
                        unit = current_config.get('profile_unit', '20ft')
                    elif cat == 'hardware':
                        unit = current_config.get('hardware_unit', 'nos')
                        if m in ['gasket', 'brush', 'red_brush', 'guide', 'jali_gasket', 'wool_pile', 'jali_angle']:
                            unit = current_config.get('linear_unit', 'ft')
                    elif m == 'glass' or m == 'labour':
                        unit = current_config.get('area_unit', 'sqft')
                    elif m == 'screw' or m == 'silicon':
                        unit = current_config.get('consumable_unit', 'set')
                        
                    formatted_materials.append({
                        "name": m,
                        "category": cat,
                        "default_unit": unit
                    })

    # Fetch additional custom materials from DB
    db_materials = db.query(MaterialRate.material_name, MaterialRate.category, MaterialRate.unit)\
        .filter(MaterialRate.user_id == current_user.id)\
        .distinct().all()

    for row in db_materials:
        if row.material_name not in seen_materials:
            seen_materials.add(row.material_name)
            formatted_materials.append({
                "name": row.material_name,
                "category": row.category or guess_category(row.material_name),
                "default_unit": row.unit or 'nos'
            })

    # Sort formatted materials
    formatted_materials.sort(key=lambda x: (x['category'] != 'profile', x['name']))

    # Fetch custom Colors and Qualities from DB
    db_colors = db.query(MaterialRate.color).filter(MaterialRate.user_id == current_user.id).distinct().all()
    db_qualities = db.query(MaterialRate.quality).filter(MaterialRate.user_id == current_user.id).distinct().all()

    default_colors = ["mill", "black", "wood", "champagne", "grey", "white"]
    all_colors = set(default_colors)
    for c in db_colors:
        if c.color:
             all_colors.add(c.color)
             
    all_qualities = set(qualities)
    for q in db_qualities:
        if q.quality:
            all_qualities.add(q.quality)

    return {
        "series": series_list,
        "qualities": sorted(list(all_qualities)),
        "materials": formatted_materials,
        "colors": sorted(list(all_colors))
    }
