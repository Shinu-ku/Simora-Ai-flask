from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SalesImportPreviewRow(BaseModel):
    date: str
    product_sku: str
    quantity: int
    unit_price: float
    unit_cost: float
    discount: float
    revenue: float

class SalesImportPreview(BaseModel):
    valid_rows: int
    invalid_rows: int
    errors: List[str]
    preview_data: List[SalesImportPreviewRow]

class SalesImportRequest(BaseModel):
    column_mapping: dict # Maps expected columns to actual CSV columns
    
class SalesRecordResponse(BaseModel):
    id: str
    business_id: str
    product_id: str
    date: datetime
    quantity: int
    unit_price: float
    unit_cost: float
    discount: float
    revenue: float
    
    class Config:
        from_attributes = True
