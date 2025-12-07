from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class VendorProfile(Base):
    __tablename__ = "vendor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    business_name = Column(String)
    address = Column(String)
    phone = Column(String)
    logo_url = Column(String, nullable=True)
    
    user = relationship("User", back_populates="vendor_profile")
