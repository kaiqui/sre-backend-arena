from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Response
import logging

logger = logging.getLogger(__name__)

ANALYSIS_COUNTER = Counter('ship_analysis_total', 'Total ship analyses', ['source'])
ANALYSIS_DURATION = Histogram('ship_analysis_duration_seconds', 'Time spent analyzing ships', buckets=(0.1, 0.5, 1.0, 2.0, 5.0))
CACHE_HITS = Counter('cache_hits_total', 'Total cache hits')
CACHE_MISSES = Counter('cache_misses_total', 'Total cache misses')
THREAT_GAUGE = Gauge('threat_level_count', 'Number of threats by level', ['level'])
API_ERRORS = Counter('api_errors_total', 'Total API errors', ['endpoint', 'status'])

def setup_prometheus(app):
    @app.get("/metrics")
    async def metrics():
        return Response(content=generate_latest(), media_type="text/plain; charset=utf-8")
    logger.info("Prometheus metrics enabled")
