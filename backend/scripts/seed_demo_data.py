import sys
import os
import random
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database.db import SessionLocal
from backend.database.models import User, Business, Product, SalesRecord
from backend.services.auth_service import get_password_hash

def seed_demo_data():
    db = SessionLocal()
    try:
        # Create user
        user = db.query(User).filter(User.email == "rajesh@demo.com").first()
        if not user:
            user = User(email="rajesh@demo.com", hashed_password=get_password_hash("demo123"))
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Created demo user")

        # Create business
        business = db.query(Business).filter(Business.owner_id == user.id).first()
        if not business:
            business = Business(
                owner_id=user.id,
                name="Rajesh Electronics",
                business_type="Retail",
                industry="Electronics",
                location="India",
                currency="INR",
                timezone="Asia/Kolkata"
            )
            db.add(business)
            db.commit()
            db.refresh(business)
            print("Created demo business")

        # Create products
        products_data = [
            {"name": "Headphones", "sku": "HP-01", "category": "Audio", "price": 4000, "cost": 2500, "stock": 150},
            {"name": "Keyboard", "sku": "KB-01", "category": "Accessories", "price": 2500, "cost": 1200, "stock": 200},
            {"name": "Mouse", "sku": "MS-01", "category": "Accessories", "price": 1200, "cost": 500, "stock": 300},
            {"name": "Smartwatch", "sku": "SW-01", "category": "Wearables", "price": 6000, "cost": 3500, "stock": 100},
            {"name": "Speaker", "sku": "SP-01", "category": "Audio", "price": 5000, "cost": 3000, "stock": 80},
            {"name": "Monitor", "sku": "MN-01", "category": "Displays", "price": 12000, "cost": 8500, "stock": 50}
        ]
        
        products = {}
        for p_data in products_data:
            product = db.query(Product).filter(Product.business_id == business.id, Product.sku == p_data["sku"]).first()
            if not product:
                product = Product(business_id=business.id, **p_data)
                db.add(product)
                db.commit()
                db.refresh(product)
            products[product.sku] = product
        print("Created products")

        # Generate 6 months of historical sales data
        # We need realistic data showing weekend effects and discount effects
        records = db.query(SalesRecord).filter(SalesRecord.business_id == business.id).first()
        if not records:
            start_date = datetime.now() - timedelta(days=180)
            sales_to_insert = []
            
            for day in range(180):
                current_date = start_date + timedelta(days=day)
                is_weekend = current_date.weekday() >= 5
                
                for sku, product in products.items():
                    # Base demand
                    base_demand = random.randint(2, 10)
                    
                    # Weekend lift (e.g. Headphones and Smartwatches sell more on weekends)
                    if is_weekend and sku in ["HP-01", "SW-01"]:
                        base_demand = int(base_demand * 1.5)
                        
                    # Occasional discounts (e.g. 10% discount)
                    discount_pct = 0
                    if random.random() < 0.1: # 10% of days have a promotion
                        discount_pct = 0.10
                        # Elasticity effect
                        base_demand = int(base_demand * 1.8)
                        
                    unit_price = product.price * (1 - discount_pct)
                    revenue = base_demand * unit_price
                    
                    if base_demand > 0:
                        sales_to_insert.append(
                            SalesRecord(
                                business_id=business.id,
                                product_id=product.id,
                                date=current_date,
                                quantity=base_demand,
                                unit_price=product.price,
                                unit_cost=product.cost,
                                discount=discount_pct,
                                revenue=revenue
                            )
                        )
            
            # Batch insert
            db.bulk_save_objects(sales_to_insert)
            db.commit()
            print(f"Created {len(sales_to_insert)} sales records")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
