from fastapi import APIRouter, HTTPException, Path
from src.services.ship_service import ship_service
from src.api.schemas.ship_analysis import ShipAnalysisResponse
from src.observability.metrics import metrics
import time

router = APIRouter(prefix="/deathstar-analysis", tags=["Death Star Analysis"])

@router.get("/{ship_id}", response_model=ShipAnalysisResponse)
async def analyze_ship(ship_id: int = Path(..., description="Ship ID from SWAPI")):
    start_time = time.time()
    
    try:
        result = await ship_service.analyze_ship(ship_id)
        
        duration_ms = (time.time() - start_time) * 1000
        metrics.record_latency("deathstar.analysis.latency", duration_ms)
        metrics.increment("deathstar.analysis.success")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        metrics.record_latency("deathstar.analysis.latency", duration_ms)
        metrics.increment("deathstar.analysis.error")
        raise HTTPException(status_code=503, detail="Service unavailable")