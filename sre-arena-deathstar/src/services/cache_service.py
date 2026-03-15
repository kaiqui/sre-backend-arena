import redis.asyncio as redis
import json
import logging
from typing import Optional, Any
from src.config.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()

class CacheService:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.ttl = settings.CACHE_TTL
        self._redis = None

    async def connect(self):
        try:
            self._redis = await redis.from_url(self.redis_url)
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")

    async def disconnect(self):
        if self._redis:
            await self._redis.close()

    async def get(self, key: str) -> Optional[Any]:
        try:
            if not self._redis:
                await self.connect()
            value = await self._redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            if not self._redis:
                await self.connect()
            ttl = ttl or self.ttl
            await self._redis.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")

    async def delete(self, key: str):
        try:
            if not self._redis:
                await self.connect()
            await self._redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")

    async def clear(self):
        try:
            if not self._redis:
                await self.connect()
            await self._redis.flushdb()
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
