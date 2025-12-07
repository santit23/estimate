from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    vendor_profile = relationship("VendorProfile", back_populates="user", uselist=False)
    material_rates = relationship("MaterialRate", back_populates="user")
    estimates = relationship("Estimate", back_populates="user")
