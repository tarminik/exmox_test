import pytest
from httpx import AsyncClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_obstacle_hit_forward_movement(async_client: AsyncClient, mock_env):
    # Move robot to position (2,4) facing EAST, then try to move forward to obstacle at (3,5) - wait that's wrong
    # Let's position robot to hit obstacle at (1,4)
    await async_client.post("/execute", json={"commands": "FFL"})  # Move to (2,2) facing SOUTH
    await async_client.post("/execute", json={"commands": "LLFF"})  # Face NORTH and move to (2,4)
    await async_client.post("/execute", json={"commands": "LFF"})  # Face WEST and move to (0,4)
    
    # Now try to move forward to obstacle at (1,4) - wait, we're at wrong position
    # Let me recalculate: start (4,2) WEST -> F -> (3,2) -> F -> (2,2) -> L -> (2,2) SOUTH
    # Let's try a simpler approach - move to position adjacent to obstacle (1,4)
    response = await async_client.post("/execute", json={"commands": "FFFR"})  # Move to (1,2) and face NORTH
    response = await async_client.post("/execute", json={"commands": "FF"})   # Move to (1,4) - this should hit obstacle
    
    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is not None
    assert "(1,4)" in data["obstacle_hit"] 
    assert "obstacle" in data["message"].lower()
    # Robot should stop before the obstacle
    assert data["final_position"]["x"] == 1
    assert data["final_position"]["y"] == 3  # Stopped at (1,3), one step before obstacle

@pytest.mark.asyncio
async def test_obstacle_hit_backward_movement(async_client: AsyncClient, mock_env):
    # Position robot at (1,5) facing SOUTH, then move backward to hit obstacle at (1,4)
    await async_client.post("/execute", json={"commands": "FFFR"})  # Move to (1,2) and face NORTH
    await async_client.post("/execute", json={"commands": "FFF"})   # Move to (1,5)
    await async_client.post("/execute", json={"commands": "LL"})    # Face SOUTH
    
    response = await async_client.post("/execute", json={"commands": "B"})  # Move backward (north) toward obstacle
    
    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is not None
    assert "(1,4)" in data["obstacle_hit"]
    assert "obstacle" in data["message"].lower()

@pytest.mark.asyncio
async def test_no_obstacle_hit_when_rotating(async_client: AsyncClient, mock_env):
    # Move to obstacle location and rotate - should not trigger obstacle detection
    await async_client.post("/execute", json={"commands": "FFFR"})  # Move to (1,2) and face NORTH
    await async_client.post("/execute", json={"commands": "FF"})    # Move to (1,4) - next to obstacle
    
    response = await async_client.post("/execute", json={"commands": "LRLR"})  # Just rotate
    
    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is None
    assert "successfully" in data["message"]

@pytest.mark.asyncio
async def test_command_execution_stops_at_first_obstacle(async_client: AsyncClient, mock_env):
    # Try to execute multiple commands but hit obstacle early
    await async_client.post("/execute", json={"commands": "FFFR"})  # Move to (1,2) and face NORTH
    
    response = await async_client.post("/execute", json={"commands": "FFFFRFLB"})  # Should stop at obstacle before completing all commands
    
    assert response.status_code == 200
    data = response.json()
    assert data["obstacle_hit"] is not None
    # Robot should not have completed the full command string

@pytest.mark.asyncio
async def test_multiple_obstacles_configuration():
    # Test with custom obstacles
    with patch.dict('os.environ', {
        'START_X': '0', 
        'START_Y': '0', 
        'START_DIRECTION': 'EAST',
        'OBSTACLES': '{(1,0), (2,0)}'
    }, clear=True):
        from httpx import AsyncClient
        from app.main import app
        from app.database import get_db
        from tests.conftest import get_db_test
        
        app.dependency_overrides[get_db] = get_db_test
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/execute", json={"commands": "F"})
            
            assert response.status_code == 200
            data = response.json()
            assert data["obstacle_hit"] is not None
            assert "(1,0)" in data["obstacle_hit"]