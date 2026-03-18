import asyncio
import time
from functools import wraps
from typing import Callable, Any
from src.config.settings import settings
from src.observability.metrics import metrics
from src.observability.logging import get_logger

logger = get_logger(__name__)

class CircuitBreaker:
    def __init__(self):
        self._state = "closed"  # closed, open, half-open
        self._failure_count = 0
        self._last_failure_time = 0
        self._error_threshold = settings.CIRCUIT_BREAKER_ERROR_THRESHOLD
        self._reset_timeout = settings.CIRCUIT_BREAKER_RESET_TIMEOUT / 1000
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self._state == "open":
            if time.time() - self._last_failure_time > self._reset_timeout:
                self._state = "half-open"
                logger.info("Circuit breaker transitioning to half-open")
                metrics.increment("circuitbreaker.half_open")
            else:
                logger.warning("Circuit breaker open - rejecting request")
                metrics.increment("circuitbreaker.reject")
                raise Exception("Circuit breaker open")
        
        try:
            result = await func(*args, **kwargs)
            if self._state == "half-open":
                self._state = "closed"
                self._failure_count = 0
                logger.info("Circuit breaker closed - success")
                metrics.increment("circuitbreaker.close")
            return result
        except Exception as e:
            self._failure_count += 1
            self._last_failure_time = time.time()
            
            if self._failure_count >= self._error_threshold:
                self._state = "open"
                logger.warning(f"Circuit breaker opened after {self._failure_count} failures")
                metrics.increment("circuitbreaker.open")
            
            raise e

circuit_breaker_instance = CircuitBreaker()

def circuit_breaker(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await circuit_breaker_instance.call(func, *args, **kwargs)
    return wrapper