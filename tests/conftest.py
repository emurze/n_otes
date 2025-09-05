from collections.abc import Callable, AsyncIterator

import pytest
from faker import Faker
from httpx import AsyncClient, ASGITransport, Headers
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from auth.adapters.jwt_adapter import JWTAdapter
from auth.adapters.password_hash_adapter import PasswordHashAdapter
from config import Config
from main import create_app
from shared.db import Base
from shared.dependencies import get_jwt_adapter
from shared.uows import SqlAlchemyUnitOfWork
from tests.auth.conftest import sign_up, login


@pytest.fixture
def config() -> Config:
    return Config()


@pytest.fixture
def engine(config: Config) -> AsyncEngine:
    return create_async_engine(
        config.db.dsn,
        poolclass=NullPool,
        echo=config.db.echo,
    )


@pytest.fixture
def session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


@pytest.fixture
async def session(session_factory: Callable) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest.fixture
async def restart_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def aclient(restart_db, config: Config) -> AsyncIterator[AsyncClient]:
    from main import create_app

    app = create_app(config)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
async def auth_client(
    restart_db,
    config: Config,
    faker: Faker,
) -> AsyncIterator[AsyncClient]:
    from main import create_app

    app = create_app(config)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as aclient:
        username = faker.user_name()
        password = faker.password()
        await sign_up(
            aclient=aclient,
            username=username,
            password=password,
        )
        tokens_response = await login(
            aclient=aclient,
            username=username,
            password=password,
        )
        access_token = tokens_response.json()["access_token"]

        headers = Headers({"Authorization": f"Bearer {access_token}"})
        aclient.headers.update(headers)
        yield aclient


@pytest.fixture
def uow(session_factory: Callable) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory)


@pytest.fixture
def ph() -> PasswordHashAdapter:
    return PasswordHashAdapter()


@pytest.fixture
def jwt_adapter(config: Config) -> JWTAdapter:
    return get_jwt_adapter(config)
