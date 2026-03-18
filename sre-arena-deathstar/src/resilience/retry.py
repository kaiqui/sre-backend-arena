import asyncio
import random
from functools import wraps
from typing import Callable, Any
from src.config.settings import settings
from src.observability.logging import get_logger

logger = get_logger(__name__)

def retry_with_backoff(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        last_exception = None
        
        for attempt in range(1, settings.RETRY_MAX_ATTEMPTS + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < settings.RETRY_MAX_ATTEMPTS:
                    # Exponential backoff with jitter
                    delay = (settings.RETRY_DELAY_MS * (2 ** (attempt - 1))) / 1000
                    jitter = random.uniform(0, delay * 0.1)
                    total_delay = delay + jitter
                    
                    logger.debug(f"Retry attempt {attempt}/{settings.RETRY_MAX_ATTEMPTS} after {total_delay:.2f}s")
                    await asyncio.sleep(total_delay)
        
        raise last_exception
    
    return wrapper