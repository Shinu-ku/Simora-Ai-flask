import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import SalesRecord, Product, DigitalTwinSnapshot

class DigitalTwinEngine:
    def __init__(self, db: Session, business_id: str):
        self.db = db
        self.business_id = business_id

    def build_twin(self) -> DigitalTwinSnapshot:
        # Fetch all sales records
        records = self.db.query(SalesRecord).filter(SalesRecord.business_id == self.business_id).all()
        if not records or len(records) < 30:
            return None # Insufficient data

        df = pd.DataFrame([{
            'date': r.date,
            'product_id': r.product_id,
            'quantity': r.quantity,
            'unit_price': r.unit_price,
            'discount': r.discount,
            'revenue': r.revenue
        } for r in records])

        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'] >= 5
        
        products = df['product_id'].unique()
        features = {
            'products': {},
            'global': {}
        }
        
        confidence_scores = []
        
        for p_id in products:
            p_df = df[df['product_id'] == p_id].copy()
            p_df = p_df.sort_values('date')
            
            if len(p_df) < 14:
                features['products'][p_id] = {'status': 'insufficient_data'}
                continue

            # Base Demand & Variance
            avg_demand = float(p_df['quantity'].mean())
            demand_variance = float(p_df['quantity'].var()) if len(p_df) > 1 else 0.0
            
            # Weekend effect
            weekend_mean = float(p_df[p_df['is_weekend']]['quantity'].mean()) if len(p_df[p_df['is_weekend']]) > 0 else avg_demand
            weekday_mean = float(p_df[~p_df['is_weekend']]['quantity'].mean()) if len(p_df[~p_df['is_weekend']]) > 0 else avg_demand
            weekend_lift = float(weekend_mean / weekday_mean) if weekday_mean > 0 else 1.0
            
            # Promotion / Discount effect (Elasticity simplified)
            # Find periods with discount vs no discount
            promo_df = p_df[p_df['discount'] > 0]
            non_promo_df = p_df[p_df['discount'] == 0]
            
            elasticity = 1.0 # default inelastic
            promo_lift = 1.0
            
            if len(promo_df) > 0 and len(non_promo_df) > 0:
                avg_promo_qty = float(promo_df['quantity'].mean())
                avg_non_promo_qty = float(non_promo_df['quantity'].mean())
                
                avg_promo_price = float(promo_df['unit_price'].mean())
                avg_non_promo_price = float(non_promo_df['unit_price'].mean())
                
                if avg_non_promo_qty > 0 and avg_non_promo_price > 0 and avg_promo_price < avg_non_promo_price:
                    pct_change_qty = (avg_promo_qty - avg_non_promo_qty) / avg_non_promo_qty
                    pct_change_price = (avg_non_promo_price - avg_promo_price) / avg_non_promo_price
                    if pct_change_price > 0:
                        elasticity = float(pct_change_qty / pct_change_price)
                        promo_lift = float(avg_promo_qty / avg_non_promo_qty)
            
            # Trend (linear slope of demand over time)
            x = np.arange(len(p_df))
            y = p_df['quantity'].values
            if len(x) > 1:
                slope, _ = np.polyfit(x, y, 1)
                trend = float(slope)
            else:
                trend = 0.0
                
            features['products'][p_id] = {
                'status': 'active',
                'avg_demand': avg_demand,
                'demand_variance': demand_variance,
                'weekend_lift': weekend_lift,
                'elasticity': max(0.0, elasticity), # elasticity should be >= 0 conceptually here
                'promo_lift': promo_lift,
                'trend': trend
            }
            
            # Confidence based on data points
            confidence_scores.append(min(1.0, len(p_df) / 100.0))
            
        overall_confidence = float(np.mean(confidence_scores)) if confidence_scores else 0.0
        
        data_quality = 'High' if overall_confidence > 0.8 else 'Medium' if overall_confidence > 0.4 else 'Low'
        
        snapshot = DigitalTwinSnapshot(
            business_id=self.business_id,
            model_version='1.0.0',
            data_range_start=df['date'].min(),
            data_range_end=df['date'].max(),
            features=features,
            confidence=overall_confidence,
            data_quality=data_quality
        )
        
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        
        return snapshot
