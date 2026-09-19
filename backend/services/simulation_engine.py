import random
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SimulationStrategy(BaseModel):
    product_id: str
    action_type: str # 'discount', 'price_change', 'restock'
    value: float
    duration_days: int

class SimulationResult(BaseModel):
    projected_units: int
    projected_revenue: float
    projected_cost: float
    projected_profit: float
    projected_margin: float
    inventory_impact: int
    risk_score: float
    confidence_score: float
    prediction_range: Dict[str, float] # min_units, max_units

class SimulationEngine:
    def __init__(self, twin_features: Dict[str, Any], current_products: List[Dict[str, Any]]):
        self.twin = twin_features
        self.products = {p['id']: p for p in current_products}

    def simulate(self, strategy: SimulationStrategy, baseline_days: int = 7, calibration_factor: float = 1.0) -> Dict[str, SimulationResult]:
        """
        Runs the simulation and returns Baseline vs Counterfactual comparison.
        """
        baseline = self._run_projection(
            baseline_days, 
            SimulationStrategy(
                product_id=strategy.product_id,
                action_type='baseline', 
                value=0.0,
                duration_days=baseline_days
            ), 
            calibration_factor=1.0
        ) # Baseline is uncalibrated
        
        counterfactual = self._run_projection(
            baseline_days, 
            strategy, 
            calibration_factor=calibration_factor
        )
        
        return {
            'baseline': baseline,
            'counterfactual': counterfactual
        }

    def _run_projection(self, days: int, strategy: SimulationStrategy, calibration_factor: float = 1.0) -> SimulationResult:
        """
        Core math engine for a single scenario using random normal sampling.
        """
        product_id = strategy.product_id
        if product_id not in self.twin['products'] or product_id not in self.products:
            raise ValueError("Product not found or has insufficient data in Digital Twin")
            
        p_twin = self.twin['products'][product_id]
        p_current = self.products[product_id]
        
        # Extract features
        avg_demand = p_twin.get('avg_demand', 0)
        variance = p_twin.get('demand_variance', 0)
        elasticity = p_twin.get('elasticity', 1.0)
        weekend_lift = p_twin.get('weekend_lift', 1.0)
        trend = p_twin.get('trend', 0.0)
        
        units = 0
        new_price = p_current['price']
        
        if strategy.action_type == 'discount':
            # discount value is percentage (e.g. 0.10)
            new_price = p_current['price'] * (1 - strategy.value)
            price_change_pct = strategy.value
            # Increase demand based on elasticity
            demand_multiplier = 1 + (price_change_pct * elasticity)
        else:
            demand_multiplier = 1.0
            
        for day in range(days):
            daily_demand = max(0, np.random.normal(avg_demand + (trend * day), np.sqrt(variance) if variance > 0 else avg_demand * 0.1))
            if day < strategy.duration_days:
                daily_demand *= demand_multiplier
            units += daily_demand
            
        # Apply Learning Loop Calibration
        total_units = int(units * calibration_factor)
        
        # Calculate financials
        projected_revenue = total_units * new_price
        projected_cost = total_units * p_current['cost']
        projected_profit = projected_revenue - projected_cost
        
        # Risk (if stock goes negative, high risk)
        current_stock = p_current['stock']
        projected_stock = current_stock - total_units
        risk_score = 0.0
        if projected_stock < 0:
            risk_score = min(1.0, abs(projected_stock) / current_stock if current_stock > 0 else 1.0)
            
        if strategy.action_type == 'baseline':
            risk_score = 0.1
            confidence_score = 0.85
        else:
            confidence_score = 0.8
            
        std_dev = np.sqrt(variance * days)
        prediction_range = {
            'min_units': max(0, total_units - int(1.96 * std_dev)),
            'max_units': total_units + int(1.96 * std_dev)
        }
        
        return SimulationResult(
            projected_units=total_units,
            projected_revenue=projected_revenue,
            projected_cost=projected_cost,
            projected_profit=projected_profit,
            projected_margin=projected_profit / projected_revenue if projected_revenue > 0 else 0,
            inventory_impact=total_units,
            risk_score=risk_score,
            confidence_score=confidence_score,
            prediction_range=prediction_range
        )
