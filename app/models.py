from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class RobotPosition(Base):
    __tablename__ = "robot_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    direction = Column(String(5), nullable=False)  # NORTH, SOUTH, EAST, WEST
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CommandExecution(Base):
    __tablename__ = "command_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    command_string = Column(Text, nullable=False)
    initial_x = Column(Integer, nullable=False)
    initial_y = Column(Integer, nullable=False)
    initial_direction = Column(String(5), nullable=False)
    final_x = Column(Integer, nullable=False)
    final_y = Column(Integer, nullable=False)
    final_direction = Column(String(5), nullable=False)
    obstacle_hit = Column(String(10), nullable=True)  # coordinates if obstacle hit
    executed_at = Column(DateTime(timezone=True), server_default=func.now())