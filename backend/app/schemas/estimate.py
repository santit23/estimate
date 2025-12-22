from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class EstimateItemBase(BaseModel):
    design: str
    series: str
    quality: str
    color: str = "mill"
    width: float
    height: float
    quantity: int

class EstimateItemCreate(EstimateItemBase):
    is_active: bool = True

class EstimateItemResponse(EstimateItemBase):
    id: int
    area: float
    unit_rate: float
    unit_rate: float
    amount: float
    is_active: bool

    class Config:
        orm_mode = True

class EstimateBase(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None

class EstimateCreate(EstimateBase):
    transport_cost: float = 0.0
    profit_margin: float = 0.0
    labour_rate: float = 0.0
    glass_rate: float = 0.0
    items: List[EstimateItemCreate]

class EstimateUpdate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    transport_cost: float = 0.0
    profit_margin: float = 0.0
    labour_rate: float = 0.0
    glass_rate: float = 0.0
    items: List[EstimateItemCreate]

class EstimateResponse(EstimateBase):
    id: int
    created_at: datetime
    total_amount: float
    total_area: float
    transport_cost: float
    profit_margin: float
    items: List[EstimateItemResponse]

    class Config:
        orm_mode = True
