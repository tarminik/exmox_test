import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_initial_position(async_client: AsyncClient, mock_env):
    response = await async_client.get("/position")
    
    assert response.status_code == 200
    data = response.json()
    assert data["x"] == 4
    assert data["y"] == 2
    assert data["direction"] == "WEST"

@pytest.mark.asyncio
async def test_get_position_returns_json_structure(async_client: AsyncClient, mock_env):
    response = await async_client.get("/position")
    
    assert response.status_code == 200
    data = response.json()
    assert "x" in data
    assert "y" in data
    assert "direction" in data
    assert isinstance(data["x"], int)
    assert isinstance(data["y"], int)
    assert isinstance(data["direction"], str)

@pytest.mark.asyncio
async def test_multiple_position_calls_consistent(async_client: AsyncClient, mock_env):
    response1 = await async_client.get("/position")
    response2 = await async_client.get("/position")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()