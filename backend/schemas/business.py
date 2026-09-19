from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusinessCreate(BaseModel):
    name: str
    business_type: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    currency: Optional[str] = "USD"
    timezone: Optional[str] = "UTC"
    business_start_date: Optional[datetime] = None

class BusinessResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    business_type: Optional[str]
    industry: Optional[str]
    location: Optional[str]
    currency: Optional[str]
    timezone: Optional[str]
    business_start_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
