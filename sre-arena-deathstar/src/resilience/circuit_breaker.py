import time
import logging
from enum import Enum
from typing import Callable, Any

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: float = 0.5, timeout: int = 60, expected_exception: Exception = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self._state = CircuitState.CLOSED

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            if self.last_failure_time and time.time() - self.last_failure_time > self.timeout:
                self._state = CircuitState.HALF_OPEN
                self.failure_count = 0
                self.success_count = 0
        return self._state

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            raise Exception("Circuit breaker is OPEN")
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            logger.info("Circuit breaker CLOSED")
        self.success_count += 1

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        total = self.failure_count + self.success_count + 1
        failure_rate = self.failure_count / total
        if failure_rate >= self.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning(f"Circuit breaker OPEN (failure_rate: {failure_rate})")
