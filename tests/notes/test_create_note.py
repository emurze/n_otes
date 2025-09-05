import pytest
from httpx import AsyncClient
from starlette import status

from tests.notes.conftest import make_note, RESOURCE


@pytest.mark.e2e
async def test_can_create_note(auth_client: AsyncClient) -> None:
    # act
    note_id = await make_note(auth_client)

    # assert
    response = await auth_client.get(f"/{RESOURCE}/{note_id}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.e2e
async def test_cannot_create_note_when_user_not_authenticated(
    aclient: AsyncClient,
) -> None:
    # act
    response = await make_note(aclient, return_response=True)

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
