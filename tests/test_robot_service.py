import pytest
from unittest.mock import patch
from app.robot_service import RobotService, Direction

@pytest.mark.asyncio
async def test_robot_service_initialization_default():
    with patch.dict('os.environ', {}, clear=True):
        service = RobotService()
        assert service.start_x == 4
        assert service.start_y == 2
        assert service.start_direction == "WEST"

@pytest.mark.asyncio
async def test_robot_service_initialization_from_env():
    with patch.dict('os.environ', {
        'START_X': '10', 
        'START_Y': '20', 
        'START_DIRECTION': 'NORTH'
    }, clear=True):
        service = RobotService()
        assert service.start_x == 10
        assert service.start_y == 20
        assert service.start_direction == "NORTH"

def test_direction_constants():
    assert Direction.NORTH == "NORTH"
    assert Direction.SOUTH == "SOUTH"
    assert Direction.EAST == "EAST"
    assert Direction.WEST == "WEST"

@pytest.mark.asyncio
async def test_obstacles_loading_default():
    with patch.dict('os.environ', {}, clear=True):
        service = RobotService()
        expected_obstacles = {(1, 4), (3, 5), (7, 4)}
        assert service.obstacles == expected_obstacles

@pytest.mark.asyncio
async def test_obstacles_loading_from_env():
    with patch.dict('os.environ', {
        'OBSTACLES': '{(2, 3), (5, 6)}'
    }, clear=True):
        service = RobotService()
        expected_obstacles = {(2, 3), (5, 6)}
        assert service.obstacles == expected_obstacles