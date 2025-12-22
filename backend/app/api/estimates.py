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
        total_area=0,
        transport_cost=estimate_in.transport_cost,
        profit_margin=estimate_in.profit_margin
    )
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    
    grand_total = 0
    grand_area = 0
    
    # Construct variable inputs for calculation
    # Only if overrides are provided (> 0)
    variable_inputs = {
        'transport_cost': estimate_in.transport_cost,
        'profit_percent': estimate_in.profit_margin
    }
    if estimate_in.labour_rate > 0:
        variable_inputs['labour_rate_sqft'] = estimate_in.labour_rate
    if estimate_in.glass_rate > 0:
        variable_inputs['glass_price'] = estimate_in.glass_rate

    # Process Items
    for item in estimate_in.items:
        # Calculate cost using the service
        try:
            # We only calculate if active? Or always calculate but only add to total if active?
            # Typically valid estimate needs valid calculation regardless of active status.
            calculation = calculate_estimate_for_item(item, current_user.id, db, variable_inputs)
        except ValueError as e:
            # Rollback and raise error if calculation fails (e.g. missing rate)
            db.delete(db_estimate)
            db.commit()
            raise HTTPException(status_code=400, detail=str(e))
            
        t_area = item.width * item.height
        
        # Note: 'total_cost' from engine ALREADY includes transport/profit logic 
        # BUT transport is usually per-estimate, not per-item in this engine's current logic?
        # Engine logic: cost_with_transport = production_cost + transport_cost
        # If we pass transport_cost to EVERY item, it multiplies transport cost by N items!
        # WARNING based on engine.py review:
        # transport_cost = vars.get('transport_cost', 0.0)
        # cost_with_transport = production_cost + transport_cost
        # YES, passing it to item calculation adds it to the item price.
        # IF the estimate has 5 items, we shouldn't add transport to each item separately if 'transport_cost' implies TOTAL transport.
        # User prompt: "optional price... transportation, profit margin(in percent)"
        # Usually transport is a fixed line item at the end.
        # ENGINE LIMITATION: Engine calculates "final_price" for the specific calculation context (1 item usually).
        # We should NOT pass transport cost to the item calculation if we want to sum them up later.
        # We should handle transport at the ESTIMATE level.
        # PROFIT however is % so it applies to each item fine.
        
        # Correction: Do NOT pass 'transport_cost' to variable_inputs for item calculation.
        # Only pass 'profit_percent', 'labour_rate_sqft', 'glass_price'.
        item_variable_inputs = variable_inputs.copy()
        if 'transport_cost' in item_variable_inputs:
            del item_variable_inputs['transport_cost']
            
        # Recalculate with corrected inputs
        try:
            calculation = calculate_estimate_for_item(item, current_user.id, db, item_variable_inputs)
        except ValueError as e:
            db.delete(db_estimate)
            db.commit()
            raise HTTPException(status_code=400, detail=str(e))

        amount = calculation['total_cost']
        unit_rate = amount / t_area if t_area > 0 else 0
        
        db_item = EstimateItem(
            estimate_id=db_estimate.id,
            design=item.design,
            series=item.series,
            quality=item.quality,
            color=item.color,
            width=item.width,
            height=item.height,
            quantity=item.quantity,
            area=t_area,
            unit_rate=unit_rate,
            amount=amount,
            is_active=item.is_active
        )
        db.add(db_item)
        
        if item.is_active:
             grand_total += amount
             grand_area += t_area
        
    # Apply Transport Cost to the Grand Total (once)
    # The 'amount' from item calculation includes profit but NOT transport (since we removed it)
    grand_total += estimate_in.transport_cost
    
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

@router.delete("/{estimate_id}")
def delete_estimate(
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
        
    # Delete associated items first (if cascade not set in model, better to be safe)
    db.query(EstimateItem).filter(EstimateItem.estimate_id == estimate_id).delete()
    
    db.delete(estimate)
    db.commit()
    
    return {"message": "Estimate deleted successfully"}

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
    estimate.transport_cost = estimate_update.transport_cost
    estimate.profit_margin = estimate_update.profit_margin
    
    # Delete old items
    db.query(EstimateItem).filter(EstimateItem.estimate_id == estimate_id).delete()
    
    # Create new items with recalculated values
    total_amount = 0.0
    total_area = 0.0
    
    # Construct variable inputs
    variable_inputs = {
        'transport_cost': estimate_update.transport_cost,
        'profit_percent': estimate_update.profit_margin
    }
    if estimate_update.labour_rate > 0:
        variable_inputs['labour_rate_sqft'] = estimate_update.labour_rate
    if estimate_update.glass_rate > 0:
        variable_inputs['glass_price'] = estimate_update.glass_rate
    
    for item_data in estimate_update.items:
        # Pass variable inputs but REMOVE transport cost for individual item calculation
        item_variable_inputs = variable_inputs.copy()
        if 'transport_cost' in item_variable_inputs:
             del item_variable_inputs['transport_cost']
             
        try:
            result = calculate_estimate_for_item(item_data, current_user.id, db, item_variable_inputs)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        area = item_data.width * item_data.height * item_data.quantity
        unit_rate = result['total_cost'] / item_data.quantity if item_data.quantity > 0 else 0
        amount = result['total_cost']
        
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
            amount=amount,
            is_active=item_data.is_active
        )
        db.add(db_item)
        
        if item_data.is_active:
             total_amount += amount
             total_area += area
    
    # Apply Transport Cost to Grand Total
    total_amount += estimate_update.transport_cost
    
    # Update totals
    estimate.total_amount = total_amount
    estimate.total_area = total_area
    
    db.commit()
    db.refresh(estimate)
    
    return estimate


# ===== FORMULA MANAGEMENT ENDPOINTS =====

@router.get("/formulas/{product_type}/{design_type}")
def get_formulas(
    product_type: str,
    design_type: str,
    current_user: User = Depends(get_current_user)
):
    """Get all formulas for a specific product type and design"""
    from app.services import core_engine_service
    from app.schemas.formula import FormulaListResponse, FormulaDisplay
    
    try:
        formulas_data = core_engine_service.get_formulas_for_display(
            product_type=product_type,
            design=design_type,
            tenant_id=str(current_user.id)
        )
        
        # Convert to response format
        formulas = {}
        for material, data in formulas_data.items():
            formulas[material] = FormulaDisplay(
                expression=data['expression'],
                description=data['description'],
                unit=data['unit'],
                constraints=data.get('constraints', {}),
                is_custom=data.get('is_custom', False),
                modified_by=data.get('modified_by'),
                modified_at=data.get('modified_at')
            )
        
        return FormulaListResponse(
            formulas=formulas,
            product_type=product_type,
            design_type=design_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/formulas/{product_type}/{design_type}/{material}")
def update_formula(
    product_type: str,
    design_type: str,
    material: str,
    formula_update: "FormulaUpdate",
    current_user: User = Depends(get_current_user)
):
    """Update a specific formula"""
    from app.services import core_engine_service
    from app.schemas.formula import FormulaUpdate
    
    try:
        success = core_engine_service.update_formula(
            product_type=product_type,
            design=design_type,
            material=material,
            expression=formula_update.expression,
            tenant_id=str(current_user.id),
            user_id=str(current_user.id)
        )
        
        return {"success": success, "message": "Formula updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formulas/{product_type}/{design_type}/{material}/reset")
def reset_formula(
    product_type: str,
    design_type: str,
    material: str,
    current_user: User = Depends(get_current_user)
):
    """Reset a formula to its default value"""
    from app.services import core_engine_service
    
    try:
        success = core_engine_service.reset_formula(
            product_type=product_type,
            design=design_type,
            material=material,
            tenant_id=str(current_user.id)
        )
        
        return {"success": success, "message": "Formula reset to default"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/formulas/{product_type}/{design_type}/{material}/validate")
def validate_formula_endpoint(
    product_type: str,
    design_type: str,
    material: str,
    validation_request: "FormulaValidationRequest",
    current_user: User = Depends(get_current_user)
):
    """Validate a formula expression"""
    from app.services import core_engine_service
    from app.schemas.formula import FormulaValidationRequest, FormulaValidationResponse
    
    try:
        result = core_engine_service.validate_formula(validation_request.expression)
        
        return FormulaValidationResponse(
            valid=result['valid'],
            error=result.get('error'),
            test_result=result.get('test_result')
        )
    except Exception as e:
        return FormulaValidationResponse(
            valid=False,
            error=str(e),
            test_result=None
        )
