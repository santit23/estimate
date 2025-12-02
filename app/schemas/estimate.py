from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class EstimateItemBase(BaseModel):
    design: str
    series: str
    quality: str
    width: float
    height: float
    quantity: int

class EstimateItemCreate(EstimateItemBase):
    pass

class EstimateItemResponse(EstimateItemBase):
    id: int
    area: float
    unit_rate: float
    amount: float

    class Config:
        orm_mode = True

class EstimateBase(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None

class EstimateCreate(EstimateBase):
    items: List[EstimateItemCreate]

class EstimateUpdate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    items: List[EstimateItemCreate]

class EstimateResponse(EstimateBase):
    id: int
    created_at: datetime
    total_amount: float
    total_area: float
    items: List[EstimateItemResponse]

    class Config:
        orm_mode = True
