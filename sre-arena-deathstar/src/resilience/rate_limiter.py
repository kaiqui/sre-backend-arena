import asyncio
import time
from functools import wraps
from typing import Callable, Any
from aiolimiter import AsyncLimiter
from src.config.settings import settings
from src.observability.logging import get_logger

logger = get_logger(__name__)

# SWAPI limit is ~1000/hour, we use 900 for safety margin
rate_limiter_instance = AsyncLimiter(
    max_rate=settings.RATE_LIMIT_PER_HOUR,
    time_period=3600  # 1 hour
)

def rate_limiter(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            async with rate_limiter_instance:
                return await func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Rate limiter error: {e}")
            raise
    
    return wrapper