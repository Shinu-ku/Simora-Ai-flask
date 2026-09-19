from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class SimulationRequest(BaseModel):
    product_id: str
    action_type: str # 'discount'
    value: float # 0.10 for 10%
    duration_days: int = 7

class SimulationResultResponse(BaseModel):
    projected_units: int
    projected_revenue: float
    projected_cost: float
    projected_profit: float
    projected_margin: float
    inventory_impact: int
    risk_score: float
    confidence_score: float
    prediction_range: Dict[str, float]

class SimulationComparisonResponse(BaseModel):
    baseline: SimulationResultResponse
    counterfactual: SimulationResultResponse
    explanation: Optional[str] = None
    ai_parsed: bool = False
    
class NaturalLanguageRequest(BaseModel):
    query: str
