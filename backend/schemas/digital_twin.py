from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class DigitalTwinResponse(BaseModel):
    id: str
    business_id: str
    model_version: str
    data_range_start: datetime
    data_range_end: datetime
    generated_at: datetime
    features: Dict[str, Any]
    confidence: float
    data_quality: str
    
    class Config:
        from_attributes = True
