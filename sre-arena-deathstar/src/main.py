import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import ddtrace

from src.config.settings import settings
from src.api.routes import health, deathstar
from src.observability.logging import setup_logging
from src.observability.metrics import setup_metrics
from src.observability.tracing import setup_tracing
from src.services.cache_service import cache_service

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Death Star Analysis API")
    setup_tracing()
    setup_metrics()
    yield
    # Shutdown
    logger.info("Shutting down Death Star Analysis API")
    await cache_service.close()

app = FastAPI(
    title="Death Star Threat Analysis API",
    description="SRE Backend Arena - Star Wars Scenario",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router, tags=["Health"])
app.include_router(deathstar.router, tags=["Death Star Analysis"])

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.get("/")
async def root():
    return {"message": "Death Star Analysis API", "version": "1.0.0"}