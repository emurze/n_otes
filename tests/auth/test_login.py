import pytest
from faker import Faker
from httpx import AsyncClient
from starlette import status

from tests.auth.conftest import sign_up, login


@pytest.mark.e2e
async def test_can_login(
    aclient: AsyncClient,
    faker: Faker,
) -> None:
    # arrange
    password = faker.password()
    username = faker.user_name()
    await sign_up(aclient, username, password)

    # act
    response = await login(aclient, username, password)
    json_response = response.json()

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert json_response["token_type"] == "Bearer"
    assert json_response["access_token"]
    assert json_response["refresh_token"]


@pytest.mark.e2e
async def test_cannot_login_using_incorrect_password(
    aclient: AsyncClient,
    faker: Faker,
) -> None:
    # arrange
    username = faker.user_name()
    await sign_up(aclient, username, password=faker.password())

    # act
    response = await login(
        aclient,
        username=username,
        password=faker.password(),
    )

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"
