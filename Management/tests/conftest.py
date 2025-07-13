import os
import warnings

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

test_url = make_url(os.environ["TEST_DATABASE_URL"])
os.environ.setdefault("DB_HOST", test_url.host or "localhost")
os.environ.setdefault("DB_PORT", str(test_url.port or 5432))
os.environ.setdefault("DB_USER", test_url.username or "postgres")
os.environ.setdefault("DB_PASSWORD", test_url.password or "")
os.environ.setdefault("DB_NAME", test_url.database or "test_db")
os.environ.setdefault("MANAGEMENT_SECRET_KEY", "secret")

warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*passlib.*")

from app.core.database import Base
from app.main import app


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture()
async def prepare_database(monkeypatch):
    engine = create_async_engine(os.environ["TEST_DATABASE_URL"])
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    class _TestDBConfig:
        def __init__(self, engine, sessionmaker):
            self.engine = engine
            self.sessionmaker = sessionmaker

    monkeypatch.setattr(
        "app.core.database.get_db_config",
        lambda: _TestDBConfig(engine, async_session),
        raising=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine, async_session
    await engine.dispose()


@pytest.fixture()
async def client(prepare_database):
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest.fixture()
async def db_session(prepare_database):
    _, async_session = prepare_database
    async with async_session() as session:
        yield session


@pytest.fixture()
async def create_test_user(db_session):
    from tests.helpers import create_user

    async def _creator(username: str, role, password: str = "Str0ng!Pass"):
        return await create_user(db_session, username, password, role)

    return _creator


@pytest.fixture()
async def get_token(client: AsyncClient):
    from tests.helpers import login

    async def _get(username: str, password: str = "Str0ng!Pass") -> str:
        return await login(client, username, password)

    return _get
