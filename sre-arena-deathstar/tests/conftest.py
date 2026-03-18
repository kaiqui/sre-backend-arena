import pytest
from httpx import AsyncClient
from src.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_ship_data():
    return {
        "name": "Death Star",
        "model": "DS-1 Orbital Battle Station",
        "crew": "342953",
        "passengers": "843342",
        "cargo_capacity": "1000000000000",
    }