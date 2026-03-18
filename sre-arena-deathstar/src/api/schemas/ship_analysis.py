from pydantic import BaseModel, Field
from typing import Optional, List

class ShipAnalysisResponse(BaseModel):
    ship: str = Field(..., description="Name of the ship")
    model: str = Field(..., description="Model designation")
    crew: int = Field(..., description="Crew size")
    passengers: int = Field(..., description="Passenger capacity")
    threatScore: int = Field(..., ge=0, le=100, description="Threat level score")
    classification: str = Field(..., description="Threat classification")