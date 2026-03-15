from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from src.config.settings import Settings
from src.api.routes import health, deathstar
from src.middleware.error_handler import ErrorHandlerMiddleware
from src.middleware.logging import LoggingMiddleware
from src.monitoring.prometheus import setup_prometheus
from src.monitoring.datadog_agent import setup_datadog
from src.monitoring.distributed_tracing import setup_tracing

settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger(__name__)
    logger.info("Starting SRE Backend Arena - Death Star Threat Analysis")
    setup_prometheus(app)
    setup_datadog()
    setup_tracing()
    yield
    logger.info("Shutting down SRE Backend Arena")

app = FastAPI(
    title="SRE Backend Arena",
    description="Death Star Threat Analysis API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(deathstar.router, prefix="/api/deathstar", tags=["deathstar"])

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower(),
    )
