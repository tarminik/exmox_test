import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_obstacle_hit_forward_movement(async_client: AsyncClient):
    await async_client.post("/execute", json={"commands": "FFFFR"})
    await async_client.post("/execute", json={"commands": "FF"})     
    await async_client.post("/execute", json={"commands": "R"})

    response = await async_client.post("/execute", json={"commands": "F"})

    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is not None
    assert "(1,4)" in data["obstacle_hit"] 
    assert "obstacle" in data["message"].lower()
    assert data["final_position"]["x"] == 0
    assert data["final_position"]["y"] == 4
    assert data["final_position"]["direction"] == "EAST"

@pytest.mark.asyncio
async def test_no_obstacle_hit_when_rotating(async_client: AsyncClient):
    await async_client.post("/execute", json={"commands": "FFFR"})
    await async_client.post("/execute", json={"commands": "FF"})

    response = await async_client.post("/execute", json={"commands": "LRLR"})

    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is None
    assert "successfully" in data["message"]

@pytest.mark.asyncio
async def test_command_execution_stops_at_first_obstacle(async_client: AsyncClient):
    await async_client.post("/execute", json={"commands": "FFFR"})

    response = await async_client.post("/execute", json={"commands": "FFFFRFLB"})

    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is not None

@pytest.mark.asyncio
async def test_multiple_obstacles_configuration(async_client: AsyncClient):
    await async_client.post("/execute", json={"commands": "FR"})

    response = await async_client.post("/execute", json={"commands": "FFF"})

    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is not None
    assert "(3,5)" in data["obstacle_hit"]