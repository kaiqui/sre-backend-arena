from datadog import initialize
import logging

logger = logging.getLogger(__name__)

def setup_datadog():
    try:
        initialize()
        logger.info("Datadog monitoring enabled")
    except Exception as e:
        logger.warning(f"Datadog initialization failed: {str(e)}")
