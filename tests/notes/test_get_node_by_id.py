import uuid

import pytest
from faker import Faker
from httpx import AsyncClient
from starlette import status

from tests.notes.conftest import make_note, RESOURCE


@pytest.mark.e2e
async def test_can_get_note_by_id(
    auth_client: AsyncClient,
    faker: Faker,
) -> None:
    # arrange
    title = faker.word()
    note_id = await make_note(auth_client, title=title)

    # act
    response = await auth_client.get(f"/{RESOURCE}/{note_id}")

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == title


@pytest.mark.e2e
async def test_cannot_get_note_by_id_when_note_not_found(
    auth_client: AsyncClient,
) -> None:
    # act
    response = await auth_client.get(f"/{RESOURCE}/{uuid.uuid4()}")

    # assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.e2e
async def test_cannot_get_note_by_id_when_user_not_authenticated(
    auth_client: AsyncClient,
    aclient: AsyncClient,
) -> None:
    # arrange
    note_id = await make_note(auth_client)

    # act
    response = await aclient.get(f"/{RESOURCE}/{note_id}")

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
