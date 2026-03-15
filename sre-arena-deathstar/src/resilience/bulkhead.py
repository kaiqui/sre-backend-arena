import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class Bulkhead:
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        async with self.semaphore:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Bulkhead error: {str(e)}")
                raise
