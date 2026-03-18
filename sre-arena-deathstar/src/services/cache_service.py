from cachetools import TTLCache
from typing import Optional, Any
import asyncio
from src.config.settings import settings
from src.observability.logging import get_logger

logger = get_logger(__name__)

class CacheService:
    def __init__(self):
        self._cache = TTLCache(
            maxsize=settings.CACHE_MAX_SIZE,
            ttl=settings.CACHE_TTL_SECONDS
        )
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            return self._cache.get(key)
    
    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            self._cache[key] = value
            logger.debug(f"Cached key: {key} (TTL: {settings.CACHE_TTL_SECONDS}s)")
    
    async def delete(self, key: str) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()
    
    async def close(self) -> None:
        await self.clear()
    
    def stats(self) -> dict:
        return {
            "size": len(self._cache),
            "max_size": settings.CACHE_MAX_SIZE,
        }

cache_service = CacheService()