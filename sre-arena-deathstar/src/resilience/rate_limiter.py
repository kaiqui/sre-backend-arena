import time
import logging
from collections import defaultdict
from typing import Dict

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.clients: Dict[str, list] = defaultdict(list)

    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        self.clients[client_id] = [t for t in self.clients[client_id] if now - t < self.window]
        if len(self.clients[client_id]) < self.requests:
            self.clients[client_id].append(now)
            return True
        logger.warning(f"Rate limit exceeded for client {client_id}")
        return False
