from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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

class VendorProfile(Base):
    __tablename__ = "vendor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    business_name = Column(String)
    address = Column(String)
    phone = Column(String)
    logo_url = Column(String, nullable=True)
    
    user = relationship("User", back_populates="vendor_profile")

class MaterialRate(Base):
    __tablename__ = "material_rates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    series = Column(String) # e.g., "90mm", "78mm"
    quality = Column(String) # e.g., "mount", "rohit"
    material_name = Column(String) # e.g., "topfr", "glass"
    rate = Column(Float)
    
    user = relationship("User", back_populates="material_rates")

class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_name = Column(String)
    customer_phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Float)
    total_area = Column(Float)
    
    user = relationship("User", back_populates="estimates")
    items = relationship("EstimateItem", back_populates="estimate")

class EstimateItem(Base):
    __tablename__ = "estimate_items"

    id = Column(Integer, primary_key=True, index=True)
    estimate_id = Column(Integer, ForeignKey("estimates.id"))
    design = Column(String) # e.g., "2panel"
    series = Column(String)
    quality = Column(String)
    width = Column(Float)
    height = Column(Float)
    quantity = Column(Integer)
    area = Column(Float)
    unit_rate = Column(Float)
    amount = Column(Float)
    
    estimate = relationship("Estimate", back_populates="items")
