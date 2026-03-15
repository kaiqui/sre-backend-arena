import pytest
import asyncio
from src.resilience.circuit_breaker import CircuitBreaker, CircuitState
from src.resilience.rate_limiter import RateLimiter

@pytest.mark.asyncio
async def test_circuit_breaker():
    async def failing_function():
        raise Exception("Test failure")

    breaker = CircuitBreaker(failure_threshold=0.5)
    for _ in range(2):
        with pytest.raises(Exception):
            await breaker.call(failing_function)
    assert breaker.state == CircuitState.OPEN

def test_rate_limiter():
    limiter = RateLimiter(requests=3, window=60)
    assert limiter.allow_request("client1") == True
    assert limiter.allow_request("client1") == True
    assert limiter.allow_request("client1") == True
    assert limiter.allow_request("client1") == False
