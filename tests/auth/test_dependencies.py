from collections.abc import AsyncGenerator

import pytest
from faker import Faker
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient, Headers
from starlette import status

from auth import services
from auth.adapters.jwt_adapter import JWTAdapter
from auth.adapters.password_hash_adapter import PasswordHashAdapter
from auth.dependencies import get_current_user
from auth.schemas import UserRead
from auth.services import authenticate_user_by_credentials
from config import Config
from shared.identity_provider import provide_identity
from shared.uows import SqlAlchemyUnitOfWork


@pytest.fixture
async def ac(config: Config) -> AsyncGenerator[AsyncClient, None]:
    app = FastAPI(config=config)

    @app.get("/me")
    async def me(user: UserRead = Depends(get_current_user)):
        return user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.mark.e2e
async def test_can_get_current_user(
    faker: Faker,
    ac: AsyncClient,
    uow: SqlAlchemyUnitOfWork,
    ph: PasswordHashAdapter,
    jwt_adapter: JWTAdapter,
    restart_db,
) -> None:
    # arrange
    username = faker.user_name()
    password = faker.password()

    await services.register_user(
        ph=ph,
        uow=uow,
        name=faker.name(),
        surname=faker.name(),
        username=username,
        password=password,
        email=faker.email(),
    )
    tokens = await authenticate_user_by_credentials(
        ph=ph,
        uow=uow,
        jwt_adapter=jwt_adapter,
        username=username,
        password=password,
    )
    access_token = tokens["access_token"]

    # act
    response = await ac.get(
        "/me",
        headers=Headers({"Authorization": f"Bearer {access_token}"}),
    )

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == username


@pytest.mark.e2e
async def test_cannot_get_current_user_when_access_token_is_invalid(
    ac: AsyncClient,
) -> None:
    # act
    invalid_token = str(provide_identity())
    response = await ac.get(
        "/me", headers=Headers({"Authorization": f"Bearer {invalid_token}"})
    )

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token is invalid"
