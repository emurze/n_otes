from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from auth.router import router
from config import Config
from shared.dependencies import get_engine


def create_app(config: Config = Config(), lifespan: Any = None) -> FastAPI:
    """
    Create and configure a FastAPI usecases with necessary middleware
    and routing, including database and resource management.
    """

    @asynccontextmanager
    async def default_lifespan(_app: FastAPI) -> AsyncIterator[None]:
        yield
        db_engine = get_engine(config=_app.extra["config"])  # type: ignore
        await db_engine.dispose()

    app = FastAPI(
        title=config.api.title,
        docs_url=config.api.docs_url,
        redoc_url=config.api.redoc_url,
        lifespan=lifespan or default_lifespan,
        config=config,
    )
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=config.api.allowed_origins,
        allow_credentials=config.api.allow_credentials,
        allow_methods=config.api.allowed_methods,
        allow_headers=config.api.allowed_headers,
    )
    app.add_middleware(
        GZipMiddleware,  # type: ignore
        minimum_size=config.api.gzip_minimum_size,
        compresslevel=config.api.gzip_compress_level,
    )
    return app
