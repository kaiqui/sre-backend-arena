import ddtrace
from src.config.settings import settings
from src.observability.logging import get_logger

logger = get_logger(__name__)

def setup_tracing() -> None:
    try:
        ddtrace.patch_all()
        logger.info("Datadog tracing initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize tracing: {e}")