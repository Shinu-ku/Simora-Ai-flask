import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api.routes import auth, business, products, sales, digital_twin, simulate, decisions, voice, memory, analytics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please try again later."},
    )

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(business.router, prefix=f"{settings.API_V1_STR}/business", tags=["business"])
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(sales.router, prefix=f"{settings.API_V1_STR}/sales", tags=["sales"])
app.include_router(digital_twin.router, prefix=f"{settings.API_V1_STR}/digital-twin", tags=["digital-twin"])
app.include_router(simulate.router, prefix=f"{settings.API_V1_STR}/simulate", tags=["simulate"])
app.include_router(decisions.router, prefix=f"{settings.API_V1_STR}/decisions", tags=["decisions"])
app.include_router(voice.router, prefix=f"{settings.API_V1_STR}/voice", tags=["voice"])
app.include_router(memory.router, prefix=f"{settings.API_V1_STR}/memory", tags=["memory"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])

@app.get("/api/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

@app.get("/api/integrations/status")
def integrations_status():
    # Placeholder for actual health checks
    return {
        "gemini": "not_configured" if not settings.GEMINI_API_KEY else "connected",
        "elevenlabs": "not_configured" if not settings.ELEVENLABS_API_KEY else "connected",
        "cognee": "not_configured" if not settings.COGNEE_API_KEY else "connected",
        "n8n": "not_configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
