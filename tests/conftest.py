import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import get_db, Base

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
async_session_maker_test = async_sessionmaker(engine_test, expire_on_commit=False)

async def get_db_test():
    async with async_session_maker_test() as session:
        yield session

@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_db] = get_db_test
    # Create tables before each test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
    # Clean up tables after each test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("START_X", "4")
    monkeypatch.setenv("START_Y", "2")
    monkeypatch.setenv("START_DIRECTION", "WEST")
    monkeypatch.setenv("OBSTACLES", "{(1,4), (3,5), (7,4)}")