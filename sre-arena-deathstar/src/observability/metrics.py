from datadog import statsd
from src.config.settings import settings
from src.observability.logging import get_logger

logger = get_logger(__name__)

class MetricsService:
    def __init__(self):
        self._initialized = False
    
    def initialize(self) -> None:
        try:
            statsd.host = settings.DD_AGENT_HOST
            statsd.port = settings.DD_DOGSTATSD_PORT
            statsd.namespace = settings.DD_SERVICE
            self._initialized = True
            logger.info(f"Metrics initialized: {settings.DD_AGENT_HOST}:{settings.DD_DOGSTATSD_PORT}")
        except Exception as e:
            logger.warning(f"Failed to initialize metrics: {e}")
    
    def increment(self, metric: str, value: int = 1, tags: list = None) -> None:
        if self._initialized:
            statsd.increment(metric, value=value, tags=tags)
    
    def record_latency(self, metric: str, duration_ms: float, tags: list = None) -> None:
        if self._initialized:
            statsd.timing(metric, duration_ms, tags=tags)
    
    def gauge(self, metric: str, value: float, tags: list = None) -> None:
        if self._initialized:
            statsd.gauge(metric, value, tags=tags)

metrics = MetricsService()

def setup_metrics() -> None:
    metrics.initialize()