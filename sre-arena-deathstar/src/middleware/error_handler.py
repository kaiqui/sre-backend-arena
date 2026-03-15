from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
            return JSONResponse(status_code=500, content={"detail": "Internal server error", "type": type(e).__name__})
