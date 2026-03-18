import httpx
import asyncio
from typing import Dict, Any
from src.config.settings import settings
from src.observability.metrics import metrics
from src.observability.logging import get_logger
from src.resilience.circuit_breaker import circuit_breaker
from src.resilience.retry import retry_with_backoff
from src.resilience.rate_limiter import rate_limiter

logger = get_logger(__name__)

class ExternalApiService:
    def __init__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.EXTERNAL_API_TIMEOUT_MS / 1000),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=50),
        )
    
    @circuit_breaker
    @retry_with_backoff
    @rate_limiter
    async def fetch_ship(self, ship_id: int) -> Dict[str, Any]:
        start_time = asyncio.get_event_loop().time()
        
        try:
            url = f"{settings.SWAPI_URL}/starships/{ship_id}/"
            response = await self._client.get(url)
            response.raise_for_status()
            
            duration_ms = (asyncio.get_event_loop().time() - start_time) * 1000
            metrics.record_latency("api.external.latency", duration_ms)
            metrics.increment("api.external.success")
            
            logger.info(f"External API call successful: ship {ship_id} ({duration_ms:.2f}ms)")
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                metrics.increment("api.external.429")
                logger.warning(f"Rate limit hit for ship {ship_id}")
            duration_ms = (asyncio.get_event_loop().time() - start_time) * 1000
            metrics.record_latency("api.external.latency", duration_ms)
            metrics.increment("api.external.error")
            logger.error(f"External API call failed: ship {ship_id}", exc_info=True)
            raise
        except Exception as e:
            duration_ms = (asyncio.get_event_loop().time() - start_time) * 1000
            metrics.record_latency("api.external.latency", duration_ms)
            metrics.increment("api.external.error")
            logger.error(f"External API call failed: ship {ship_id}", exc_info=True)
            raise
    
    async def close(self) -> None:
        await self._client.aclose()

external_api_service = ExternalApiService()