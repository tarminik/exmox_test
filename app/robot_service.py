import os
from typing import Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import RobotPosition, CommandExecution
from app.schemas import RobotPositionResponse

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