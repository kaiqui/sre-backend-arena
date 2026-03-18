import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_analyze_ship_success(client: AsyncClient):
    response = await client.get("/deathstar-analysis/9")
    assert response.status_code == 200
    data = response.json()
    assert "ship" in data
    assert "threatScore" in data
    assert "classification" in data
    assert 0 <= data["threatScore"] <= 100

@pytest.mark.asyncio
async def test_analyze_ship_invalid_id(client: AsyncClient):
    response = await client.get("/deathstar-analysis/999999")
    assert response.status_code in [404, 503]

@pytest.mark.asyncio
async def test_health_live(client: AsyncClient):
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_health_ready(client: AsyncClient):
    response = await client.get("/health/ready")
    assert response.status_code in [200, 503]