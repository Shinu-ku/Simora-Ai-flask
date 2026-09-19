from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DecisionCreate(BaseModel):
    product_id: str
    action_type: str
    value: float
    duration_days: int
    predicted_units: int
    predicted_revenue: float
    predicted_profit: float

class DecisionResponse(BaseModel):
    id: str
    business_id: str
    product_id: str
    action_type: str
    value: float
    duration_days: int
    status: str
    predicted_units: int
    predicted_revenue: float
    predicted_profit: float
    actual_units: Optional[int]
    actual_revenue: Optional[float]
    actual_profit: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
