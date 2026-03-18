import pytest
from unittest.mock import AsyncMock, patch
from src.services.ship_service import ship_service

@pytest.mark.asyncio
async def test_calculate_threat_score_death_star():
    ship_data = {
        "name": "Death Star",
        "crew": "342953",
        "passengers": "843342",
        "cargo_capacity": "1000000000000",
    }
    score = ship_service._calculate_threat_score(ship_data)
    assert score >= 90

@pytest.mark.asyncio
async def test_classify_threat_superweapon():
    classification = ship_service._classify_threat(95)
    assert classification == "galactic_superweapon"

@pytest.mark.asyncio
async def test_classify_threat_capital_ship():
    classification = ship_service._classify_threat(75)
    assert classification == "capital_ship"

@pytest.mark.asyncio
async def test_classify_threat_fighter():
    classification = ship_service._classify_threat(20)
    assert classification == "fighter"