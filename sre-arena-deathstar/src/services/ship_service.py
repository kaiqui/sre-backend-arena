from src.services.external_api_service import external_api_service
from src.services.cache_service import cache_service
from src.observability.metrics import metrics
from src.api.schemas.ship_analysis import ShipAnalysisResponse
from src.observability.logging import get_logger

logger = get_logger(__name__)

class ShipService:
    async def analyze_ship(self, ship_id: int) -> ShipAnalysisResponse:
        cache_key = f"ship:{ship_id}"
        
        # Check cache first
        cached = await cache_service.get(cache_key)
        if cached:
            logger.debug(f"Cache hit for ship: {ship_id}")
            metrics.increment("ship.cache.hit")
            return cached
        
        metrics.increment("ship.cache.miss")
        logger.debug(f"Cache miss for ship: {ship_id}")
        
        # Fetch from external API
        ship_data = await external_api_service.fetch_ship(ship_id)
        
        # Calculate threat score
        threat_score = self._calculate_threat_score(ship_data)
        classification = self._classify_threat(threat_score)
        
        result = ShipAnalysisResponse(
            ship=ship_data["name"],
            model=ship_data["model"],
            crew=int(ship_data.get("crew", 0) or 0),
            passengers=int(ship_data.get("passengers", 0) or 0),
            threatScore=threat_score,
            classification=classification,
        )
        
        # Cache the result
        await cache_service.set(cache_key, result)
        
        logger.info(f"Ship analysis completed: {ship_data['name']} (threat: {threat_score})")
        return result
    
    def _calculate_threat_score(self, ship_data: dict) -> int:
        crew = int(ship_data.get("crew", 0) or 0)
        passengers = int(ship_data.get("passengers", 0) or 0)
        cargo_capacity = int(ship_data.get("cargo_capacity", 0) or 0)
        
        # Base score from crew size
        score = min(50, crew / 10000)
        
        # Add passenger factor
        score += min(20, passengers / 50000)
        
        # Add cargo capacity factor
        score += min(20, cargo_capacity / 1000000)
        
        # Bonus for known superweapons
        name_lower = ship_data.get("name", "").lower()
        if "death star" in name_lower:
            score += 10
        if "star destroyer" in name_lower:
            score += 5
        
        return int(min(100, max(0, score)))
    
    def _classify_threat(self, score: int) -> str:
        if score >= 90:
            return "galactic_superweapon"
        elif score >= 70:
            return "capital_ship"
        elif score >= 50:
            return "cruiser"
        elif score >= 30:
            return "frigate"
        else:
            return "fighter"

ship_service = ShipService()