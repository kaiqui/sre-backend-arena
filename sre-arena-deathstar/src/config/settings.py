from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "SRE Backend Arena"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = ["*"]
    STAR_WARS_API_BASE_URL: str = "https://swapi.dev/api"
    STAR_WARS_API_TIMEOUT: int = 10
    CACHE_TTL: int = 3600
    REDIS_URL: str = "redis://localhost:6379"
    CIRCUIT_BREAKER_THRESHOLD: float = 0.5
    CIRCUIT_BREAKER_TIMEOUT: int = 60
    RETRY_MAX_ATTEMPTS: int = 3
    RETRY_BACKOFF: float = 2.0
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    PROMETHEUS_ENABLED: bool = True
    DATADOG_ENABLED: bool = True
    DATADOG_API_KEY: str = ""
    DATADOG_APP_KEY: str = ""
    TRACING_ENABLED: bool = True
    JAEGER_HOST: str = "localhost"
    JAEGER_PORT: int = 6831
    SLO_AVAILABILITY: float = 0.9999
    SLO_LATENCY_P99: float = 0.5

    class Config:
        env_file = ".env"
        case_sensitive = True
