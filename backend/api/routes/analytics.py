from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
from datetime import datetime, timedelta
from backend.database.db import get_db
from backend.database.models import User, SalesRecord as Sale, Product
from backend.services.auth_service import get_current_user

router = APIRouter()

def get_current_business(current_user: User = Depends(get_current_user)):
    return current_user.business

@router.get("/")
def get_analytics(
    timeframe: str = Query("30D", description="7D, 30D, 90D, 6M"),
    business=Depends(get_current_business), 
    db: Session = Depends(get_db)
):
    days_map = {"7D": 7, "30D": 30, "90D": 90, "6M": 180}
    days = days_map.get(timeframe, 30)
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Let's get the sales for this period for this business
    sales = db.query(
        func.sum(Sale.units).label('units'),
        func.sum(Sale.revenue).label('revenue'),
        func.sum(Sale.cost).label('cost')
    ).join(Product).filter(
        Product.business_id == business.id,
        Sale.date >= start_date
    ).first()
    
    units = sales.units or 0
    revenue = sales.revenue or 0.0
    cost = sales.cost or 0.0
    profit = revenue - cost
    aov = revenue / units if units > 0 else 0.0
    margin = profit / revenue if revenue > 0 else 0.0
    
    # For chart data (daily aggregation)
    daily_sales = db.query(
        func.date(Sale.date).label('day'),
        func.sum(Sale.revenue).label('revenue'),
        func.sum(Sale.revenue - Sale.cost).label('profit')
    ).join(Product).filter(
        Product.business_id == business.id,
        Sale.date >= start_date
    ).group_by(func.date(Sale.date)).order_by(func.date(Sale.date)).all()
    
    chart_data = [{"date": row.day, "revenue": row.revenue, "profit": row.profit} for row in daily_sales]
    
    return {
        "summary": {
            "units": units,
            "revenue": revenue,
            "profit": profit,
            "aov": aov,
            "margin": margin
        },
        "chart": chart_data
    }
