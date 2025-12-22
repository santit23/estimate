from typing import Dict, Optional
from pydantic import BaseModel


class FormulaDisplay(BaseModel):
    """Formula metadata for UI display"""
    expression: str
    description: str
    unit: str
    constraints: Dict
    is_custom: bool = False
    modified_by: Optional[str] = None
    modified_at: Optional[str] = None


class FormulaListResponse(BaseModel):
    """Dictionary of formulas for a design"""
    formulas: Dict[str, FormulaDisplay]
    product_type: str
    design_type: str


class FormulaUpdate(BaseModel):
    """Request body for updating a formula"""
    expression: str


class FormulaValidationRequest(BaseModel):
    """Request body for validating a formula"""
    expression: str


class FormulaValidationResponse(BaseModel):
    """Response for formula validation"""
    valid: bool
    error: Optional[str] = None
    test_result: Optional[float] = None
