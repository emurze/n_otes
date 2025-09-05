from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from starlette.requests import Request

from auth.adapters.jwt_adapter import JWTAdapter
from auth.adapters.password_hash_adapter import PasswordHashAdapter
from config import Config
from shared.uows import SqlAlchemyUnitOfWork


def get_config(request: Request) -> Config:
    return request.app.extra["config"]


def get_engine(config: Config = Depends(get_config)) -> AsyncEngine:
    return create_async_engine(config.db.dsn, echo=False)


def get_session_factory(engine: AsyncEngine = Depends(get_engine)) -> Callable:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def get_uow(
    session_factory: Callable = Depends(get_session_factory),
) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session_factory=session_factory)


def get_ph() -> PasswordHashAdapter:
    return PasswordHashAdapter()


def get_jwt_adapter(config: Config = Depends(get_config)) -> JWTAdapter:
    return JWTAdapter(
        secret=config.jwt.secret_key,
        algorithm=config.jwt.algorithm,
        token_type_key=config.jwt.token_type_key,
        refresh_token_type=config.jwt.refresh_token_type,
        access_token_type=config.jwt.access_token_type,
        refresh_token_expire_days=config.jwt.refresh_token_expire_days,
        access_token_expire_minutes=config.jwt.access_token_expire_minutes,
    )
