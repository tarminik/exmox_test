from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RobotPositionResponse(BaseModel):
    x: int
    y: int
    direction: str
    
class CommandRequest(BaseModel):
    commands: str
    
class CommandResponse(BaseModel):
    initial_position: RobotPositionResponse
    final_position: RobotPositionResponse
    obstacle_hit: Optional[str] = None
    message: str