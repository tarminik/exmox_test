import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine, Base
from app.robot_service import RobotService
from app.schemas import RobotPositionResponse, CommandRequest, CommandResponse


# We use FastAPI lifespan handlers instead of deprecated on_event hooks

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan.

    - On startup (before yielding): optionally create DB tables if explicitly
      enabled via RUN_DB_SETUP environment variable. This avoids touching the
      real database during tests, keeping tests fast and isolated.
    - On shutdown (after yield): currently no cleanup required.
    """
    run_db_setup = os.getenv("RUN_DB_SETUP", "0").lower() in {"1", "true", "yes"}
    if run_db_setup:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # No shutdown actions needed for now

app = FastAPI(title="Moon Robot Control API", version="1.0.0", lifespan=lifespan)
robot_service = RobotService()

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