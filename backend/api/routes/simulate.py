from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import User, DigitalTwinSnapshot, Product
from backend.schemas.simulation import SimulationRequest, SimulationComparisonResponse, NaturalLanguageRequest
from backend.services.auth_service import get_current_user
from backend.services.simulation_engine import SimulationEngine, SimulationStrategy
from backend.services.ai_parser import AIParserService
from backend.services.memory_engine import MemoryEngine

router = APIRouter()
ai_parser = AIParserService()

def get_current_business(current_user: User = Depends(get_current_user)):
    if not current_user.business:
        raise HTTPException(status_code=400, detail="User does not have a business")
    return current_user.business

@router.post("/", response_model=SimulationComparisonResponse)
def run_simulation(request: SimulationRequest, business=Depends(get_current_business), db: Session = Depends(get_db)):
    # 1. Retrieve Latest Digital Twin
    twin = db.query(DigitalTwinSnapshot).filter(DigitalTwinSnapshot.business_id == business.id).order_by(DigitalTwinSnapshot.generated_at.desc()).first()
    if not twin:
        raise HTTPException(status_code=400, detail="No Digital Twin found. Please generate one first.")
        
    # 2. Retrieve Product state
    products = db.query(Product).filter(Product.business_id == business.id).all()
    products_data = [{
        'id': p.id,
        'sku': p.sku,
        'price': p.price,
        'cost': p.cost,
        'stock': p.stock
    } for p in products]
    
    # 3. Run Simulation
    engine = SimulationEngine(twin.features, products_data)
    strategy = SimulationStrategy(
        product_id=request.product_id,
        action_type=request.action_type,
        value=request.value,
        duration_days=request.duration_days
    )
    
    # Get calibration factor from Learning Loop
    memory_engine = MemoryEngine(db, business.id)
    cal_factor = memory_engine.get_calibration(strategy.action_type)
    
    try:
        results = engine.simulate(strategy, baseline_days=request.duration_days, calibration_factor=cal_factor)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/natural-language", response_model=SimulationComparisonResponse)
def run_natural_language_simulation(request: NaturalLanguageRequest, business=Depends(get_current_business), db: Session = Depends(get_db)):
    # 1. Parse intent
    parsed = ai_parser.parse_scenario(request.query)
    
    # 2. Find product
    products = db.query(Product).filter(Product.business_id == business.id).all()
    target_product = None
    search_term = parsed.product_name_or_sku.lower()
    for p in products:
        if search_term in p.name.lower() or search_term in p.sku.lower():
            target_product = p
            break
            
    if not target_product:
        # Fallback to the first product if we can't find a match (demo behavior)
        if products:
            target_product = products[0]
        else:
            raise HTTPException(status_code=400, detail="No products found to run simulation.")

    # 3. Build structured request
    sim_req = SimulationRequest(
        product_id=target_product.id,
        action_type=parsed.action_type,
        value=parsed.value,
        duration_days=parsed.duration_days
    )
    
    # 4. Run standard simulation
    result = run_simulation(sim_req, business, db)
    
    # 5. Add AI fields (explanation omitted for now unless we add an AI summarizer)
    result['ai_parsed'] = True
    result['explanation'] = f"Parsed intent: {parsed.action_type} by {parsed.value*100}% on {target_product.name} for {parsed.duration_days} days. Using elasticities and trend from Digital Twin."
    
    return result
