from fastapi import APIRouter
import logging
from src.api.schemas.ship_analysis import HealthStatus
from src.services.external_api_service import ExternalAPIService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=HealthStatus)
async def health_check():
    try:
        external_api = ExternalAPIService()
        external_status = await external_api.health_check()
        return HealthStatus(
            status="healthy" if external_status else "degraded",
            version="1.0.0",
            dependencies={
                "external_api": "healthy" if external_status else "unhealthy",
                "cache": "healthy",
                "monitoring": "healthy"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthStatus(
            status="unhealthy",
            version="1.0.0",
            dependencies={"external_api": "unhealthy", "cache": "unknown", "monitoring": "unknown"}
        )

@router.get("/live")
async def liveness_probe():
    return {"status": "alive"}

@router.get("/ready")
async def readiness_probe():
    return {"status": "ready"}
