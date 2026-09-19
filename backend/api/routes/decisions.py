from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.db import get_db
from backend.database.models import User, Decision
from backend.schemas.decision import DecisionCreate, DecisionResponse
from backend.services.auth_service import get_current_user
from pydantic import BaseModel
from backend.services.executor import DemoExecutor
from backend.services.memory_engine import MemoryEngine

executor = DemoExecutor()

class OutcomeRequest(BaseModel):
    actual_units: int
    actual_revenue: float
    actual_profit: float

router = APIRouter()

def get_current_business(current_user: User = Depends(get_current_user)):
    if not current_user.business:
        raise HTTPException(status_code=400, detail="User does not have a business")
    return current_user.business

@router.post("/", response_model=DecisionResponse)
def create_decision(decision_in: DecisionCreate, business=Depends(get_current_business), db: Session = Depends(get_db)):
    decision = Decision(
        business_id=business.id,
        product_id=decision_in.product_id,
        action_type=decision_in.action_type,
        value=decision_in.value,
        duration_days=decision_in.duration_days,
        predicted_units=decision_in.predicted_units,
        predicted_revenue=decision_in.predicted_revenue,
        predicted_profit=decision_in.predicted_profit,
        status="PENDING"
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision

@router.get("/", response_model=List[DecisionResponse])
def get_decisions(business=Depends(get_current_business), db: Session = Depends(get_db)):
    return db.query(Decision).filter(Decision.business_id == business.id).order_by(Decision.created_at.desc()).all()

@router.post("/{decision_id}/approve", response_model=DecisionResponse)
def approve_decision(decision_id: str, business=Depends(get_current_business), db: Session = Depends(get_db)):
    decision = db.query(Decision).filter(Decision.id == decision_id, Decision.business_id == business.id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    if decision.status != "PENDING":
        raise HTTPException(status_code=400, detail="Only PENDING decisions can be approved")
        
    decision.status = "APPROVED"
    db.commit()
    db.refresh(decision)
    
    # Ideally, we trigger execution here
    return decision

@router.post("/{decision_id}/execute", response_model=DecisionResponse)
def execute_decision(decision_id: str, business=Depends(get_current_business), db: Session = Depends(get_db)):
    decision = db.query(Decision).filter(Decision.id == decision_id, Decision.business_id == business.id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
        
    if decision.status != "APPROVED":
        raise HTTPException(status_code=400, detail="Decision must be APPROVED before execution")
        
    # Simulate execution using DemoExecutor
    payload = {
        "action": decision.action_type,
        "value": decision.value,
        "product_id": decision.product_id
    }
    result = executor.execute(decision.id, payload)
    
    decision.status = "EXECUTED"
    db.commit()
    db.refresh(decision)
    
    # We could optionally attach the executor message to the response if needed.
    return decision

@router.post("/{decision_id}/reject", response_model=DecisionResponse)
def reject_decision(decision_id: str, business=Depends(get_current_business), db: Session = Depends(get_db)):
    decision = db.query(Decision).filter(Decision.id == decision_id, Decision.business_id == business.id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
        
    if decision.status != "PENDING":
        raise HTTPException(status_code=400, detail="Only PENDING decisions can be rejected")
        
    decision.status = "REJECTED"
    db.commit()
    db.refresh(decision)
    
    return decision

@router.post("/{decision_id}/outcome", response_model=DecisionResponse)
def record_outcome(decision_id: str, request: OutcomeRequest, business=Depends(get_current_business), db: Session = Depends(get_db)):
    decision = db.query(Decision).filter(Decision.id == decision_id, Decision.business_id == business.id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
        
    if decision.status != "EXECUTED":
        raise HTTPException(status_code=400, detail="Can only record outcomes for EXECUTED decisions")
        
    decision.actual_units = request.actual_units
    decision.actual_revenue = request.actual_revenue
    decision.actual_profit = request.actual_profit
    
    # Trigger Learning Loop
    memory_engine = MemoryEngine(db, business.id)
    memory_engine.process_outcome(decision)
    
    db.commit()
    db.refresh(decision)
    
    return decision
