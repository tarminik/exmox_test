import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_execute_forward_command(async_client: AsyncClient):
    response = await async_client.post("/execute", json={"commands": "F"})

    assert response.status_code == 200
    data = response.json()
    assert data["initial_position"]["x"] == 4
    assert data["initial_position"]["y"] == 2
    assert data["initial_position"]["direction"] == "WEST"
    assert data["final_position"]["x"] == 3
    assert data["final_position"]["y"] == 2
    assert data["final_position"]["direction"] == "WEST"
    assert data["obstacle_hit"] is None
    assert "successfully" in data["message"]

@pytest.mark.asyncio
async def test_execute_backward_command(async_client: AsyncClient):
    response = await async_client.post("/execute", json={"commands": "B"})

    assert response.status_code == 200
    data = response.json()
    assert data["final_position"]["x"] == 5
    assert data["final_position"]["y"] == 2
    assert data["final_position"]["direction"] == "WEST"

@pytest.mark.asyncio
async def test_execute_left_rotation(async_client: AsyncClient):
    response = await async_client.post("/execute", json={"commands": "L"})

    assert response.status_code == 200
    data = response.json()
    assert data["final_position"]["x"] == 4
    assert data["final_position"]["y"] == 2
    assert data["final_position"]["direction"] == "SOUTH"

@pytest.mark.asyncio
async def test_execute_right_rotation(async_client: AsyncClient):
    response = await async_client.post("/execute", json={"commands": "R"})

    assert response.status_code == 200
    data = response.json()
    assert data["final_position"]["x"] == 4
    assert data["final_position"]["y"] == 2
    assert data["final_position"]["direction"] == "NORTH"

@pytest.mark.asyncio
async def test_execute_complex_command_string(async_client: AsyncClient):
    response = await async_client.post("/execute", json={"commands": "FLFFFRFLB"})

    assert response.status_code == 200
    data = response.json()
    assert data["initial_position"]["x"] == 4
    assert data["initial_position"]["y"] == 2
    assert data["initial_position"]["direction"] == "WEST"
    assert data["obstacle_hit"] is None

@pytest.mark.asyncio
async def test_execute_case_insensitive_commands(async_client: AsyncClient):
    response = await async_client.post("/execute", json={"commands": "flr"})

    assert response.status_code == 200
    data = response.json()
    assert data["final_position"]["direction"] == "WEST"
    assert data["final_position"]["x"] == 3

@pytest.mark.asyncio
async def test_robot_state_persists_between_calls(async_client: AsyncClient):
    response1 = await async_client.post("/execute", json={"commands": "F"})
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["final_position"]["x"] == 3

    response2 = await async_client.post("/execute", json={"commands": "F"})
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["initial_position"]["x"] == 3
    assert data2["final_position"]["x"] == 2

@pytest.mark.asyncio
async def test_position_endpoint_reflects_command_execution(async_client: AsyncClient):
    await async_client.post("/execute", json={"commands": "FFR"})

    position_response = await async_client.get("/position")
    assert position_response.status_code == 200

    position_data = position_response.json()
    assert position_data["x"] == 2 
    assert position_data["y"] == 2
    assert position_data["direction"] == "NORTH"