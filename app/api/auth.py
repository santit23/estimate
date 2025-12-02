from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.models import User, VendorProfile, MaterialRate
from app.schemas.user import UserCreate, Token
from config import MATERIAL_RATES # Import legacy rates to seed new vendors

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    # Create User
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create Vendor Profile
    vendor_profile = VendorProfile(
        user_id=user.id,
        business_name=user_in.business_name,
        address=user_in.address,
        phone=user_in.phone
    )
    db.add(vendor_profile)
    
    # Seed Material Rates from default config
    # We flatten the nested structure for the DB
    for series, qualities in MATERIAL_RATES.items():
        for quality, materials in qualities.items():
            for mat_name, rate in materials.items():
                db_rate = MaterialRate(
                    user_id=user.id,
                    series=series,
                    quality=quality,
                    material_name=mat_name,
                    rate=float(rate)
                )
                db.add(db_rate)
    
    db.commit()
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
