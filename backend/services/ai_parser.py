from google import genai
from pydantic import BaseModel
from typing import Optional
from backend.config import settings
from backend.schemas.simulation import SimulationRequest

class ParsedScenario(BaseModel):
    product_name_or_sku: str
    action_type: str
    value: float
    duration_days: int

class AIParserService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def parse_scenario(self, user_query: str) -> ParsedScenario:
        if not self.client:
            return self._fallback_parse(user_query)

        prompt = f"""
You are SIMORA, a Business Decision Simulation Engine.
Extract the scenario from the user's query.

User Query: "{user_query}"

Return a JSON object matching this schema exactly:
{{
  "product_name_or_sku": "string",
  "action_type": "discount", 
  "value": float (e.g. 0.10 for 10% discount),
  "duration_days": integer (e.g. 2 for weekend, 7 for a week)
}}
"""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': ParsedScenario,
                    'temperature': 0.1
                }
            )
            # The google-genai client returns the pydantic object in parsed
            return response.parsed
        except Exception as e:
            print(f"Gemini API error: {e}, using fallback parser.")
            return self._fallback_parse(user_query)

    def _fallback_parse(self, user_query: str) -> ParsedScenario:
        """Deterministic fallback parser if Gemini fails or is not configured."""
        q = user_query.lower()
        action = "discount"
        value = 0.10
        duration = 7
        
        if "weekend" in q:
            duration = 2
        elif "month" in q:
            duration = 30
            
        import re
        match = re.search(r'(\d+)%', q)
        if match:
            value = float(match.group(1)) / 100.0

        product = "unknown"
        if "headphone" in q:
            product = "Headphones"
        elif "laptop" in q:
            product = "Laptop"

        return ParsedScenario(
            product_name_or_sku=product,
            action_type=action,
            value=value,
            duration_days=duration
        )
