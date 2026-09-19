import json
from sqlalchemy.orm import Session
from backend.database.models import Memory, Calibration, Decision
from backend.config import settings

class MemoryEngine:
    def __init__(self, db: Session, business_id: str):
        self.db = db
        self.business_id = business_id
        self.use_cognee = bool(settings.COGNEE_API_KEY)

    def process_outcome(self, decision: Decision):
        """Analyzes outcome and updates calibration and memory."""
        
        # 1. Calculate Error
        if decision.predicted_units == 0:
            return
            
        error_pct = (decision.actual_units - decision.predicted_units) / decision.predicted_units
        
        # 2. Update Calibration (Learning Loop)
        cal = self.db.query(Calibration).filter(
            Calibration.business_id == self.business_id,
            Calibration.action_type == decision.action_type
        ).first()
        
        if not cal:
            cal = Calibration(
                business_id=self.business_id,
                action_type=decision.action_type,
                sample_count=0,
                average_error=0.0,
                calibration_factor=1.0,
                version=1
            )
            self.db.add(cal)
            
        # Do not recalibrate aggressively from one isolated observation.
        # Moving average error
        old_error = cal.average_error
        cal.average_error = (old_error * cal.sample_count + error_pct) / (cal.sample_count + 1)
        cal.sample_count += 1
        
        # New calibration factor: if we consistently overpredict, factor should be < 1
        # Factor = 1 + average_error. Example: average_error = -0.2 (underperformed 20%). Factor = 0.8
        # We dampen the learning rate (0.5) so it doesn't swing wildly
        learning_rate = 0.5
        cal.calibration_factor = 1.0 + (cal.average_error * learning_rate)
        cal.version += 1
        
        # 3. Store Memory
        if self.use_cognee:
            self._store_cognee_memory(decision, error_pct)
        else:
            self._store_local_memory(decision, error_pct, cal.calibration_factor)
            
        self.db.commit()

    def _store_local_memory(self, decision: Decision, error_pct: float, factor: float):
        observation = f"Observed {decision.action_type} outcome: {decision.actual_units} units vs {decision.predicted_units} predicted. Error: {error_pct*100:.1f}%."
        mem = Memory(
            business_id=self.business_id,
            memory_type="OBSERVATION",
            content=observation,
            metadata_json={"error": error_pct, "new_factor": factor, "product_id": decision.product_id}
        )
        self.db.add(mem)

    def _store_cognee_memory(self, decision: Decision, error_pct: float):
        # Placeholder for Cognee integration
        # In a real scenario we'd use the cognee SDK to append the memory graph
        pass

    def get_calibration(self, action_type: str) -> float:
        cal = self.db.query(Calibration).filter(
            Calibration.business_id == self.business_id,
            Calibration.action_type == action_type
        ).first()
        return cal.calibration_factor if cal else 1.0
