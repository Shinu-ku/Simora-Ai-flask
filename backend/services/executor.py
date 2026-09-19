class BaseExecutor:
    def execute(self, decision_id: str, payload: dict) -> dict:
        raise NotImplementedError

class DemoExecutor(BaseExecutor):
    def execute(self, decision_id: str, payload: dict) -> dict:
        print(f"[DemoExecutor] Executing decision {decision_id} with {payload}")
        return {
            "status": "success",
            "message": "Simulated execution. No real action occurred."
        }

class N8NExecutor(BaseExecutor):
    def execute(self, decision_id: str, payload: dict) -> dict:
        # In a real app, send HTTP POST to n8n webhook
        # requests.post(settings.N8N_WEBHOOK_URL, json=payload)
        return {
            "status": "error",
            "message": "N8N integration not configured."
        }
