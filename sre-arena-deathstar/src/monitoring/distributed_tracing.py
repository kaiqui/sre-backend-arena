from jaeger_client import Config
import logging

logger = logging.getLogger(__name__)

def setup_tracing():
    try:
        config = Config(
            config={'sampler': {'type': 'const', 'param': 1}, 'logging': True},
            service_name='sre-backend-arena',
        )
        config.initialize_tracer()
        logger.info("Distributed tracing enabled")
    except Exception as e:
        logger.warning(f"Tracing initialization failed: {str(e)}")
