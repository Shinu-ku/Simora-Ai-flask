from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import User, Business
from backend.schemas.business import BusinessCreate, BusinessResponse
from backend.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=BusinessResponse)
def create_business(business: BusinessCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.business:
        raise HTTPException(status_code=400, detail="User already has a business")
    
    new_business = Business(
        owner_id=current_user.id,
        name=business.name,
        business_type=business.business_type,
        industry=business.industry,
        location=business.location,
        currency=business.currency,
        timezone=business.timezone,
        business_start_date=business.business_start_date
    )
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return new_business

@router.get("/", response_model=BusinessResponse)
def get_business(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.business:
        raise HTTPException(status_code=404, detail="Business not found")
    return current_user.business
