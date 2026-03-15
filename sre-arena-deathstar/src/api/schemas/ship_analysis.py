from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ThreatLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

class ShipAnalysis(BaseModel):
    ship_id: str = Field(..., description="Unique ship identifier")
    ship_name: str = Field(..., description="Name of the ship")
    threat_level: ThreatLevel = Field(..., description="Threat level classification")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    estimated_damage_potential: float = Field(..., description="Estimated damage potential")
    weaponry_assessment: str = Field(..., description="Assessment of weaponry")
    armor_rating: float = Field(..., ge=0, le=10, description="Armor rating (0-10)")
    speed_rating: float = Field(..., ge=0, le=10, description="Speed rating (0-10)")
    tactical_recommendations: List[str] = Field(default_factory=list)
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)
    cache_hit: bool = Field(default=False, description="Whether response was from cache")

class HealthStatus(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(..., description="API version")
    dependencies: dict = Field(default_factory=dict)
