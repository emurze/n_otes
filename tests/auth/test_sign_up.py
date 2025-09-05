import pytest
from faker import Faker
from httpx import AsyncClient
from starlette import status

from tests.auth.conftest import sign_up


@pytest.mark.e2e
async def test_can_sign_up(aclient: AsyncClient, faker: Faker) -> None:
    # arrange
    username = faker.user_name()
    password = faker.password()
    email = faker.email()

    # act
    response = await sign_up(aclient, username, password, email)

    # assert
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.e2e
async def test_cannot_sign_up_when_username_already_exists(
    aclient: AsyncClient,
    faker: Faker,
) -> None:
    # arrange
    username = faker.user_name()
    await sign_up(aclient, username=username)

    # act
    response = await sign_up(aclient, username=username)

    # assert
    assert response.status_code == status.HTTP_409_CONFLICT
