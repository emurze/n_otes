import pytest
from httpx import AsyncClient
from starlette import status

from tests.auth.conftest import sign_up, RESOURCE


@pytest.mark.e2e
async def test_can_refresh_tokens(aclient: AsyncClient) -> None:
    # arrange
    response = await sign_up(aclient)
    refresh_token = response.json()["refresh_token"]

    # act
    response = await aclient.post(
        f"{RESOURCE}/refresh-token",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    json_response = response.json()

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert json_response["token_type"] == "Bearer"
    assert json_response["access_token"]
    assert json_response["refresh_token"]


@pytest.mark.e2e
async def test_cannot_refresh_without_token(aclient: AsyncClient) -> None:
    # act
    response = await aclient.post(f"{RESOURCE}/refresh-token")

    # assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
