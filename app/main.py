from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine, Base
from app.robot_service import RobotService
from app.schemas import RobotPositionResponse

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