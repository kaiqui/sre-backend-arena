from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.3f}s")
        return response
