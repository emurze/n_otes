import pytest
from httpx import AsyncClient
from starlette import status

from tests.notes.conftest import make_note, RESOURCE


@pytest.mark.e2e
async def test_can_delete_note(auth_client: AsyncClient) -> None:
    # act
    note_id = await make_note(auth_client)

    # assert
    response = await auth_client.delete(f"/{RESOURCE}/{note_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # by checking tha note does not exist
    response = await auth_client.get(f"/{RESOURCE}/{note_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.e2e
async def test_cannot_delete_note_when_user_not_authenticated(
    aclient: AsyncClient,
) -> None:
    # act
    response = await make_note(aclient, return_response=True)

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
