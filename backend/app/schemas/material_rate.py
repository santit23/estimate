from typing import List, Optional
from pydantic import BaseModel

class MaterialRateBase(BaseModel):
    series: str
    quality: str
    color: str
    material_name: str
    unit: Optional[str] = None
    category: Optional[str] = "other"
    rate: float

class MaterialRateCreate(MaterialRateBase):
    pass

class MaterialRateUpdate(BaseModel):
    id: Optional[int] = None
    series: str
    quality: str
    color: str
    material_name: str
    unit: Optional[str] = None
    category: Optional[str] = "other"
    rate: float

class MaterialRateResponse(MaterialRateBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class BulkRateUpdate(BaseModel):
    rates: List[MaterialRateUpdate]
