import aiohttp
import asyncio
import logging
from typing import Optional, Dict
from src.config.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()

class ExternalAPIService:
    def __init__(self):
        self.base_url = settings.STAR_WARS_API_BASE_URL
        self.timeout = settings.STAR_WARS_API_TIMEOUT

    async def get_ship(self, ship_id: str) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/starships/{ship_id}/"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        logger.warning(f"Ship {ship_id} not found")
                        return None
                    else:
                        raise Exception(f"API returned {response.status}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching ship {ship_id}")
            raise
        except Exception as e:
            logger.error(f"Error fetching ship {ship_id}: {str(e)}")
            raise

    async def health_check(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
