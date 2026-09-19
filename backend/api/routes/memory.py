from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database.db import get_db
from backend.database.models import User, Memory, Calibration
from backend.services.auth_service import get_current_user
from pydantic import BaseModel
from datetime import datetime

class MemoryResponse(BaseModel):
    id: str
    memory_type: str
    content: str
    metadata_json: dict | None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CalibrationResponse(BaseModel):
    action_type: str
    sample_count: int
    average_error: float
    calibration_factor: float
    version: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

router = APIRouter()

def get_current_business(current_user: User = Depends(get_current_user)):
    return current_user.business

@router.get("/", response_model=List[MemoryResponse])
def get_memories(business=Depends(get_current_business), db: Session = Depends(get_db)):
    return db.query(Memory).filter(Memory.business_id == business.id).order_by(Memory.created_at.desc()).all()

@router.get("/calibrations", response_model=List[CalibrationResponse])
def get_calibrations(business=Depends(get_current_business), db: Session = Depends(get_db)):
    return db.query(Calibration).filter(Calibration.business_id == business.id).all()
