from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MaterialRate(Base):
    __tablename__ = "material_rates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    series = Column(String)  # e.g., "90mm", "78mm"
    quality = Column(String)  # e.g., "mount", "rohit"
    material_name = Column(String)  # e.g., "topfr", "glass"
    rate = Column(Float)
    
    user = relationship("User", back_populates="material_rates")
