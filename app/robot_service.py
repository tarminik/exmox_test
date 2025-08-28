import os
from typing import Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import RobotPosition, CommandExecution
from app.schemas import RobotPositionResponse, CommandResponse

class Direction:
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

class RobotService:
    def __init__(self):
        self.start_x = int(os.getenv("START_X", "4"))
        self.start_y = int(os.getenv("START_Y", "2"))
        self.start_direction = os.getenv("START_DIRECTION", "WEST")
        self.obstacles = self._load_obstacles()
    
    def _load_obstacles(self) -> set:
        obstacles_str = os.getenv("OBSTACLES", "{(1,4), (3,5), (7,4)}")
        obstacles = set()
        try:
            obstacles = eval(obstacles_str)
        except:
            obstacles = {(1, 4), (3, 5), (7, 4)}
        return obstacles
    
    async def get_current_position(self, db: AsyncSession) -> RobotPositionResponse:
        result = await db.execute(
            select(RobotPosition).order_by(desc(RobotPosition.created_at)).limit(1)
        )
        latest_position = result.scalar_one_or_none()
        
        if latest_position is None:
            await self._initialize_position(db)
            return RobotPositionResponse(
                x=self.start_x, 
                y=self.start_y, 
                direction=self.start_direction
            )
        
        return RobotPositionResponse(
            x=latest_position.x,
            y=latest_position.y,
            direction=latest_position.direction
        )
    
    async def _initialize_position(self, db: AsyncSession):
        initial_position = RobotPosition(
            x=self.start_x,
            y=self.start_y,
            direction=self.start_direction
        )
        db.add(initial_position)
        await db.commit()
        return initial_position
    
    async def update_position(self, db: AsyncSession, x: int, y: int, direction: str):
        new_position = RobotPosition(x=x, y=y, direction=direction)
        db.add(new_position)
        await db.commit()
        return new_position
    
    def _rotate_left(self, direction: str) -> str:
        rotation_map = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH
        }
        return rotation_map[direction]
    
    def _rotate_right(self, direction: str) -> str:
        rotation_map = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH
        }
        return rotation_map[direction]
    
    def _move_forward(self, x: int, y: int, direction: str) -> Tuple[int, int]:
        if direction == Direction.NORTH:
            return x, y + 1
        elif direction == Direction.SOUTH:
            return x, y - 1
        elif direction == Direction.EAST:
            return x + 1, y
        elif direction == Direction.WEST:
            return x - 1, y
        return x, y
    
    def _move_backward(self, x: int, y: int, direction: str) -> Tuple[int, int]:
        if direction == Direction.NORTH:
            return x, y - 1
        elif direction == Direction.SOUTH:
            return x, y + 1
        elif direction == Direction.EAST:
            return x - 1, y
        elif direction == Direction.WEST:
            return x + 1, y
        return x, y
    
    async def execute_commands(self, db: AsyncSession, command_string: str) -> CommandResponse:
        current_pos = await self.get_current_position(db)
        initial_position = RobotPositionResponse(
            x=current_pos.x,
            y=current_pos.y,
            direction=current_pos.direction
        )
        
        x, y, direction = current_pos.x, current_pos.y, current_pos.direction
        obstacle_hit = None
        
        for command in command_string.upper():
            if command == 'F':
                new_x, new_y = self._move_forward(x, y, direction)
                if (new_x, new_y) in self.obstacles:
                    obstacle_hit = f"({new_x},{new_y})"
                    break
                x, y = new_x, new_y
            elif command == 'B':
                new_x, new_y = self._move_backward(x, y, direction)
                if (new_x, new_y) in self.obstacles:
                    obstacle_hit = f"({new_x},{new_y})"
                    break
                x, y = new_x, new_y
            elif command == 'L':
                direction = self._rotate_left(direction)
            elif command == 'R':
                direction = self._rotate_right(direction)
        
        await self.update_position(db, x, y, direction)
        
        command_execution = CommandExecution(
            command_string=command_string,
            initial_x=initial_position.x,
            initial_y=initial_position.y,
            initial_direction=initial_position.direction,
            final_x=x,
            final_y=y,
            final_direction=direction,
            obstacle_hit=obstacle_hit
        )
        db.add(command_execution)
        await db.commit()
        
        final_position = RobotPositionResponse(x=x, y=y, direction=direction)
        
        message = "Commands executed successfully"
        if obstacle_hit:
            message = f"Stopped due to obstacle at {obstacle_hit}"
        
        return CommandResponse(
            initial_position=initial_position,
            final_position=final_position,
            obstacle_hit=obstacle_hit,
            message=message
        )