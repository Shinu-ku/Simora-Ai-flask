from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    sku: str
    category: Optional[str] = None
    price: float
    cost: float
    stock: Optional[int] = 0
    reorder_threshold: Optional[int] = 0
    status: Optional[str] = "active"

class ProductResponse(ProductCreate):
    id: str
    business_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    stock: Optional[int] = None
    reorder_threshold: Optional[int] = None
    status: Optional[str] = None
