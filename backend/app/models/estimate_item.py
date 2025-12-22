from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class EstimateItem(Base):
    __tablename__ = "estimate_items"

    id = Column(Integer, primary_key=True, index=True)
    estimate_id = Column(Integer, ForeignKey("estimates.id"))
    design = Column(String)  # e.g., "2panel"
    series = Column(String)
    quality = Column(String)
    color = Column(String, default="mill")
    width = Column(Float)
    height = Column(Float)
    quantity = Column(Integer)
    area = Column(Float)
    unit_rate = Column(Float)
    amount = Column(Float)
    is_active = Column(Boolean, default=True)
    
    estimate = relationship("Estimate", back_populates="items")
