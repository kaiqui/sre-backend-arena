from typing import List, Dict
import logging
from datetime import datetime

from src.api.schemas.ship_analysis import ShipAnalysis, ThreatLevel
from src.services.external_api_service import ExternalAPIService
from src.resilience.circuit_breaker import CircuitBreaker
from src.resilience.retry import retry

logger = logging.getLogger(__name__)

class ShipService:
    def __init__(self):
        self.external_api = ExternalAPIService()
        self.circuit_breaker = CircuitBreaker(failure_threshold=0.5, timeout=60)

    @retry(max_attempts=3, backoff=2.0)
    async def analyze_ship(self, ship_id: str) -> ShipAnalysis:
        ship_data = await self.circuit_breaker.call(self.external_api.get_ship, ship_id)
        if not ship_data:
            raise ValueError(f"Ship {ship_id} not found")
        threat_level, risk_score = self._calculate_threat(ship_data)
        analysis = ShipAnalysis(
            ship_id=ship_id,
            ship_name=ship_data.get("name", "Unknown"),
            threat_level=threat_level,
            risk_score=risk_score,
            estimated_damage_potential=self._calculate_damage(ship_data),
            weaponry_assessment=self._assess_weaponry(ship_data),
            armor_rating=self._calculate_armor(ship_data),
            speed_rating=self._calculate_speed(ship_data),
            tactical_recommendations=self._generate_recommendations(threat_level, ship_data),
            analyzed_at=datetime.utcnow()
        )
        logger.info(f"Analyzed ship {ship_id} with threat level {threat_level}")
        return analysis

    def _calculate_threat(self, ship_data: Dict) -> tuple:
        cost = float(ship_data.get("cost_in_credits", 0) or 0)
        crew = int(ship_data.get("crew", 0) or 0)
        risk_score = min(100, (crew * 0.5) + (cost / 1000000))
        if risk_score >= 80:
            threat_level = ThreatLevel.CRITICAL
        elif risk_score >= 60:
            threat_level = ThreatLevel.HIGH
        elif risk_score >= 40:
            threat_level = ThreatLevel.MEDIUM
        elif risk_score >= 20:
            threat_level = ThreatLevel.LOW
        else:
            threat_level = ThreatLevel.MINIMAL
        return threat_level, risk_score

    def _calculate_damage(self, ship_data: Dict) -> float:
        cargo_capacity = float(ship_data.get("cargo_capacity", 0) or 0)
        max_speed = int(ship_data.get("max_atmosphering_speed", 0) or 0)
        return (cargo_capacity / 100000) * (max_speed / 1000)

    def _assess_weaponry(self, ship_data: Dict) -> str:
        ship_class = ship_data.get("starship_class", "Unknown")
        if "fighter" in ship_class.lower():
            return "Light weaponry, suitable for patrol and escort"
        elif "cruiser" in ship_class.lower():
            return "Medium to heavy weaponry, suitable for frontline combat"
        return "Unknown weaponry configuration"

    def _calculate_armor(self, ship_data: Dict) -> float:
        return min(10, len(ship_data.get("name", "")) / 3)

    def _calculate_speed(self, ship_data: Dict) -> float:
        speed = int(ship_data.get("max_atmosphering_speed", 0) or 0)
        return min(10, speed / 1000)

    def _generate_recommendations(self, threat_level: ThreatLevel, ship_data: Dict) -> List[str]:
        recommendations = []
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.append("Escalate to highest alert status")
            recommendations.append("Deploy defensive systems immediately")
            recommendations.append("Request reinforcements")
        elif threat_level == ThreatLevel.HIGH:
            recommendations.append("Increase monitoring frequency")
            recommendations.append("Prepare defensive countermeasures")
        return recommendations

    async def get_threats_by_level(self, level: ThreatLevel) -> List[ShipAnalysis]:
        return []

    async def get_threat_statistics(self) -> Dict:
        return {"total_ships_analyzed": 0, "critical_count": 0, "high_count": 0, "average_risk_score": 0.0}
