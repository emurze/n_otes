import pytest
from faker import Faker
from httpx import AsyncClient
from starlette import status

from tests.auth.conftest import sign_up, login
from tests.notes.conftest import make_note, RESOURCE


@pytest.mark.e2e
async def test_can_get_notes(
    auth_client: AsyncClient,
    faker: Faker,
) -> None:
    # arrange
    title = faker.word()
    title2 = faker.word()
    await make_note(auth_client, title=title)
    await make_note(auth_client, title=title2)

    # act
    response = await auth_client.get(RESOURCE)

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert title in str(response.json())
    assert title2 in str(response.json())


@pytest.mark.e2e
async def test_can_get_only_user_notes(
    auth_client: AsyncClient,
    faker: Faker,
) -> None:
    # arrange
    user1_headers = auth_client.headers["Authorization"]

    # by creating the second user
    username = faker.user_name()
    password = faker.password()
    await sign_up(
        aclient=auth_client,
        username=username,
        password=password,
    )
    tokens_response = await login(
        aclient=auth_client,
        username=username,
        password=password,
    )
    access_token = tokens_response.json()["access_token"]
    auth_client.headers["Authorization"] = f"Bearer {access_token}"

    # by creating two notes for the second user
    await make_note(auth_client)
    await make_note(auth_client)

    # by switching to the first user
    auth_client.headers["Authorization"] = user1_headers

    # by creating one note for the first user
    title = faker.name()
    await make_note(auth_client, title=title)

    # act
    response = await auth_client.get(RESOURCE)

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert title in str(response.json())


@pytest.mark.e2e
async def test_cannot_get_notes_when_user_not_authenticated(
    auth_client: AsyncClient,
    aclient: AsyncClient,
) -> None:
    # arrange
    await make_note(auth_client)

    # act
    response = await aclient.get(f"/{RESOURCE}")

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
