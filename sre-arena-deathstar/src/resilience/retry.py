import asyncio
import logging
import random
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, backoff: float = 2.0, jitter: bool = True, exceptions: tuple = (Exception,)):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            last_exception = None
            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    attempt += 1
                    if attempt < max_attempts:
                        wait_time = backoff ** (attempt - 1)
                        if jitter:
                            wait_time += random.uniform(0, wait_time * 0.1)
                        logger.warning(f"Attempt {attempt} failed for {func.__name__}, retrying in {wait_time:.2f}s")
                        await asyncio.sleep(wait_time)
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator
