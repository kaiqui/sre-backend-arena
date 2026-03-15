from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging

from src.api.schemas.ship_analysis import ShipAnalysis, ThreatLevel
from src.services.ship_service import ShipService
from src.services.cache_service import CacheService
from src.resilience.rate_limiter import RateLimiter
from src.monitoring.prometheus import ANALYSIS_COUNTER, ANALYSIS_DURATION

router = APIRouter()
logger = logging.getLogger(__name__)

ship_service = ShipService()
cache_service = CacheService()
rate_limiter = RateLimiter()

@router.post("/analyze/{ship_id}", response_model=ShipAnalysis)
async def analyze_ship(ship_id: str, force_refresh: bool = Query(False)):
    if not rate_limiter.allow_request(client_id="global"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    try:
        cache_key = f"ship_analysis:{ship_id}"
        if not force_refresh:
            cached_analysis = await cache_service.get(cache_key)
            if cached_analysis:
                logger.info(f"Cache hit for ship {ship_id}")
                ANALYSIS_COUNTER.labels(source="cache").inc()
                return cached_analysis
        with ANALYSIS_DURATION.time():
            analysis = await ship_service.analyze_ship(ship_id)
        await cache_service.set(cache_key, analysis, ttl=3600)
        ANALYSIS_COUNTER.labels(source="api").inc()
        return analysis
    except ValueError as e:
        logger.warning(f"Invalid ship: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/ships/critical", response_model=List[ShipAnalysis])
async def get_critical_threats():
    try:
        return await ship_service.get_threats_by_level(ThreatLevel.CRITICAL)
    except Exception as e:
        logger.error(f"Failed to fetch critical threats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/threat-statistics")
async def get_threat_statistics():
    try:
        return await ship_service.get_threat_statistics()
    except Exception as e:
        logger.error(f"Failed to fetch statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
