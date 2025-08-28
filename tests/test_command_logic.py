import pytest
from app.robot_service import RobotService, Direction

def test_rotate_left_logic():
    service = RobotService()
    
    assert service._rotate_left(Direction.NORTH) == Direction.WEST
    assert service._rotate_left(Direction.WEST) == Direction.SOUTH
    assert service._rotate_left(Direction.SOUTH) == Direction.EAST
    assert service._rotate_left(Direction.EAST) == Direction.NORTH

def test_rotate_right_logic():
    service = RobotService()
    
    assert service._rotate_right(Direction.NORTH) == Direction.EAST
    assert service._rotate_right(Direction.EAST) == Direction.SOUTH
    assert service._rotate_right(Direction.SOUTH) == Direction.WEST
    assert service._rotate_right(Direction.WEST) == Direction.NORTH

def test_move_forward_logic():
    service = RobotService()
    
    assert service._move_forward(0, 0, Direction.NORTH) == (0, 1)
    assert service._move_forward(0, 0, Direction.SOUTH) == (0, -1)
    assert service._move_forward(0, 0, Direction.EAST) == (1, 0)
    assert service._move_forward(0, 0, Direction.WEST) == (-1, 0)

def test_move_backward_logic():
    service = RobotService()
    
    assert service._move_backward(0, 0, Direction.NORTH) == (0, -1)
    assert service._move_backward(0, 0, Direction.SOUTH) == (0, 1)
    assert service._move_backward(0, 0, Direction.EAST) == (-1, 0)
    assert service._move_backward(0, 0, Direction.WEST) == (1, 0)

def test_full_rotation_cycle():
    service = RobotService()
    
    direction = Direction.NORTH
    # Four left rotations should return to original direction
    for _ in range(4):
        direction = service._rotate_left(direction)
    assert direction == Direction.NORTH
    
    direction = Direction.NORTH
    # Four right rotations should return to original direction
    for _ in range(4):
        direction = service._rotate_right(direction)
    assert direction == Direction.NORTH

def test_movement_coordinates():
    service = RobotService()
    
    # Test movement from different starting positions
    assert service._move_forward(5, 5, Direction.NORTH) == (5, 6)
    assert service._move_forward(5, 5, Direction.EAST) == (6, 5)
    assert service._move_backward(5, 5, Direction.NORTH) == (5, 4)
    assert service._move_backward(5, 5, Direction.WEST) == (6, 5)