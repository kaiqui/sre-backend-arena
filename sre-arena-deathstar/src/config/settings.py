from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "production"
    
    # Datadog
    DD_API_KEY: str = ""
    DD_APP_KEY: str = ""
    DD_ENV: str = "production"
    DD_SERVICE: str = "deathstar-analysis-api"
    DD_VERSION: str = "1.0.0"
    DD_AGENT_HOST: str = "localhost"
    DD_DOGSTATSD_PORT: int = 8125
    
    # External API
    SWAPI_URL: str = "https://swapi.dev/api"
    EXTERNAL_API_TIMEOUT_MS: int = 2000
    RATE_LIMIT_PER_HOUR: int = 900
    
    # Cache
    CACHE_TTL_SECONDS: int = 300
    CACHE_MAX_SIZE: int = 1000
    
    # Circuit Breaker
    CIRCUIT_BREAKER_TIMEOUT: int = 3000
    CIRCUIT_BREAKER_ERROR_THRESHOLD: int = 50
    CIRCUIT_BREAKER_RESET_TIMEOUT: int = 30000
    
    # Retry
    RETRY_MAX_ATTEMPTS: int = 3
    RETRY_DELAY_MS: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()