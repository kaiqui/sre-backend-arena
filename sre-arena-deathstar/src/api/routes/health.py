from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.config.settings import settings
import httpx

router = APIRouter(tags=["Health"])

@router.get("/health/live")
async def liveness():
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness():
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            await client.get(f"{settings.SWAPI_URL}/")
        return {"status": "ready", "external_api": "up"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "external_api": "down"},
        )