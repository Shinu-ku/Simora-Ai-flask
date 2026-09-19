from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Dict
import pandas as pd
import io
import json
from datetime import datetime
from backend.database.db import get_db
from backend.database.models import User, Product, SalesRecord
from backend.schemas.sales import SalesImportPreview, SalesRecordResponse
from backend.services.auth_service import get_current_user

router = APIRouter()

def get_current_business(current_user: User = Depends(get_current_user)):
    if not current_user.business:
        raise HTTPException(status_code=400, detail="User does not have a business")
    return current_user.business

@router.post("/import", response_model=SalesImportPreview)
async def import_sales_data(
    file: UploadFile = File(...),
    column_mapping: str = Form(...),
    business=Depends(get_current_business),
    db: Session = Depends(get_db)
):
    try:
        mapping = json.loads(column_mapping)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid column mapping format")

    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to parse CSV")

    required_fields = ['date', 'product', 'quantity', 'unit_price', 'unit_cost', 'revenue']
    for field in required_fields:
        if field not in mapping or mapping[field] not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing mapped column for {field}")

    valid_rows = 0
    invalid_rows = 0
    errors = []
    
    # We will just do a simple import for now
    product_cache = {}
    db_products = db.query(Product).filter(Product.business_id == business.id).all()
    for p in db_products:
        product_cache[p.sku] = p.id
        product_cache[p.name] = p.id
        
    for index, row in df.iterrows():
        try:
            prod_val = str(row[mapping['product']])
            product_id = product_cache.get(prod_val)
            if not product_id:
                invalid_rows += 1
                errors.append(f"Row {index}: Product {prod_val} not found")
                continue
                
            date_val = pd.to_datetime(row[mapping['date']])
            
            record = SalesRecord(
                business_id=business.id,
                product_id=product_id,
                date=date_val,
                quantity=int(row[mapping['quantity']]),
                unit_price=float(row[mapping['unit_price']]),
                unit_cost=float(row[mapping['unit_cost']]),
                discount=float(row.get(mapping.get('discount'), 0.0) if 'discount' in mapping and pd.notna(row.get(mapping['discount'])) else 0.0),
                revenue=float(row[mapping['revenue']])
            )
            db.add(record)
            valid_rows += 1
        except Exception as e:
            invalid_rows += 1
            errors.append(f"Row {index}: Error parsing data - {str(e)}")

    if valid_rows > 0:
        db.commit()

    return {
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "errors": errors[:10], # limit error return
        "preview_data": []
    }

@router.get("/", response_model=List[SalesRecordResponse])
def get_sales(business=Depends(get_current_business), db: Session = Depends(get_db)):
    records = db.query(SalesRecord).filter(SalesRecord.business_id == business.id).limit(100).all()
    return records
