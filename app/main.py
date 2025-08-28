from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine, Base
from app.robot_service import RobotService
from app.schemas import RobotPositionResponse, CommandRequest, CommandResponse

app = FastAPI(title="Moon Robot Control API", version="1.0.0")
robot_service = RobotService()

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Moon Robot Control API"}

@app.get("/position", response_model=RobotPositionResponse)
async def get_position(db: AsyncSession = Depends(get_db)):
    return await robot_service.get_current_position(db)

@app.post("/execute", response_model=CommandResponse)
async def execute_commands(
    request: CommandRequest, 
    db: AsyncSession = Depends(get_db)
):
    return await robot_service.execute_commands(db, request.commands)