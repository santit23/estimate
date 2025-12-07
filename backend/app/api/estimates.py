from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.models import User, Estimate, EstimateItem
from app.schemas.estimate import EstimateCreate, EstimateResponse, EstimateUpdate
from app.services.estimator_service import calculate_estimate_for_item

router = APIRouter()

@router.post("/", response_model=EstimateResponse)
def create_estimate(
    estimate_in: EstimateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create Estimate Header
    db_estimate = Estimate(
        user_id=current_user.id,
        customer_name=estimate_in.customer_name,
        customer_phone=estimate_in.customer_phone,
        total_amount=0,
        total_area=0
    )
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    
    grand_total = 0
    grand_area = 0
    
    # Process Items
    for item in estimate_in.items:
        # Calculate cost using the service
        try:
            calculation = calculate_estimate_for_item(item, current_user.id, db)
        except ValueError as e:
            # Rollback and raise error if calculation fails (e.g. missing rate)
            db.delete(db_estimate)
            db.commit()
            raise HTTPException(status_code=400, detail=str(e))
            
        t_area = item.width * item.height
        amount = calculation['total_cost']
        unit_rate = amount / t_area if t_area > 0 else 0
        
        db_item = EstimateItem(
            estimate_id=db_estimate.id,
            design=item.design,
            series=item.series,
            quality=item.quality,
            width=item.width,
            height=item.height,
            quantity=item.quantity,
            area=t_area,
            unit_rate=unit_rate,
            amount=amount
        )
        db.add(db_item)
        
        grand_total += amount
        grand_area += t_area
        
    # Update Estimate Totals
    db_estimate.total_amount = grand_total
    db_estimate.total_area = grand_area
    db.commit()
    db.refresh(db_estimate)
    
    return db_estimate

@router.get("/", response_model=List[EstimateResponse])
def read_estimates(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    estimates = db.query(Estimate).filter(Estimate.user_id == current_user.id).offset(skip).limit(limit).all()
    return estimates

@router.get("/{estimate_id}", response_model=EstimateResponse)
def read_estimate(
    estimate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    estimate = db.query(Estimate).filter(
        Estimate.id == estimate_id,
        Estimate.user_id == current_user.id
    ).first()
    
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    return estimate

@router.put("/{estimate_id}", response_model=EstimateResponse)
def update_estimate(
    estimate_id: int,
    estimate_update: EstimateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    estimate = db.query(Estimate).filter(
        Estimate.id == estimate_id,
        Estimate.user_id == current_user.id
    ).first()
    
    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")
    
    # Update customer information
    estimate.customer_name = estimate_update.customer_name
    estimate.customer_phone = estimate_update.customer_phone
    
    # Delete old items
    db.query(EstimateItem).filter(EstimateItem.estimate_id == estimate_id).delete()
    
    # Create new items with recalculated values
    total_amount = 0.0
    total_area = 0.0
    
    for item_data in estimate_update.items:
        result = calculate_estimate_for_item(item_data, current_user.id, db)
        
        area = item_data.width * item_data.height * item_data.quantity
        unit_rate = result['total'] / item_data.quantity if item_data.quantity > 0 else 0
        amount = result['total']
        
        db_item = EstimateItem(
            estimate_id=estimate.id,
            design=item_data.design,
            series=item_data.series,
            quality=item_data.quality,
            width=item_data.width,
            height=item_data.height,
            quantity=item_data.quantity,
            area=area,
            unit_rate=unit_rate,
            amount=amount
        )
        db.add(db_item)
        
        total_amount += amount
        total_area += area
    
    # Update totals
    estimate.total_amount = total_amount
    estimate.total_area = total_area
    
    db.commit()
    db.refresh(estimate)
    
    return estimate
