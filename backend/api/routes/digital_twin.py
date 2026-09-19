from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import User, DigitalTwinSnapshot
from backend.schemas.digital_twin import DigitalTwinResponse
from backend.services.auth_service import get_current_user
from backend.services.digital_twin import DigitalTwinEngine

router = APIRouter()

def get_current_business(current_user: User = Depends(get_current_user)):
    if not current_user.business:
        raise HTTPException(status_code=400, detail="User does not have a business")
    return current_user.business

@router.post("/generate", response_model=DigitalTwinResponse)
def generate_twin(business=Depends(get_current_business), db: Session = Depends(get_db)):
    engine = DigitalTwinEngine(db, business.id)
    snapshot = engine.build_twin()
    if not snapshot:
        raise HTTPException(status_code=400, detail="Insufficient historical evidence.")
    return snapshot

@router.get("/latest", response_model=DigitalTwinResponse)
def get_latest_twin(business=Depends(get_current_business), db: Session = Depends(get_db)):
    snapshot = db.query(DigitalTwinSnapshot)\
                 .filter(DigitalTwinSnapshot.business_id == business.id)\
                 .order_by(DigitalTwinSnapshot.generated_at.desc())\
                 .first()
    if not snapshot:
        raise HTTPException(status_code=404, detail="No digital twin found")
    return snapshot
