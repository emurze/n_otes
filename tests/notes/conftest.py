from uuid import UUID

from faker import Faker
from httpx import AsyncClient, Response

RESOURCE = "notes"


async def make_note(
    auth_client: AsyncClient,
    faker: Faker | None = None,
    title: str | None = None,
    content: str | None = None,
    return_response: bool = False,
) -> UUID | Response:
    faker = faker or Faker()
    response = await auth_client.post(
        f"/{RESOURCE}",
        json={
            "title": title or faker.name(),
            "content": content or faker.text(),
        },
    )

    if return_response:
        return response

    return response.json()["id"]
