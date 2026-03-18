import pytest
from src.services.cache_service import cache_service

@pytest.mark.asyncio
async def test_cache_set_get():
    await cache_service.set("test_key", {"value": "test"})
    result = await cache_service.get("test_key")
    assert result == {"value": "test"}

@pytest.mark.asyncio
async def test_cache_miss():
    result = await cache_service.get("nonexistent_key")
    assert result is None

@pytest.mark.asyncio
async def test_cache_delete():
    await cache_service.set("delete_key", {"value": "test"})
    await cache_service.delete("delete_key")
    result = await cache_service.get("delete_key")
    assert result is None