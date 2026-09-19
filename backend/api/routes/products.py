from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database.db import get_db
from backend.database.models import User, Product
from backend.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from backend.services.auth_service import get_current_user

router = APIRouter()

def get_current_business(current_user: User = Depends(get_current_user)):
    if not current_user.business:
        raise HTTPException(status_code=400, detail="User does not have a business")
    return current_user.business

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, business=Depends(get_current_business), db: Session = Depends(get_db)):
    new_product = Product(**product.model_dump(), business_id=business.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductResponse])
def get_products(business=Depends(get_current_business), db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.business_id == business.id).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, business=Depends(get_current_business), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.business_id == business.id, Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product_update: ProductUpdate, business=Depends(get_current_business), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.business_id == business.id, Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: str, business=Depends(get_current_business), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.business_id == business.id, Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"status": "success"}
