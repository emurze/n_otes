from faker import Faker
from httpx import AsyncClient, Response

RESOURCE = "auth"


async def login(
    aclient: AsyncClient,
    username: str | None = None,
    password: str | None = None,
) -> Response:
    faker = Faker()
    return await aclient.post(
        f"{RESOURCE}/login",
        data={
            "username": username or faker.name(),
            "password": password or faker.password(),
        },
    )


async def sign_up(
    aclient: AsyncClient,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
) -> Response:
    faker = Faker()
    return await aclient.post(
        f"{RESOURCE}/signup",
        json={
            "name": faker.name(),
            "surname": faker.name(),
            "username": username or faker.name(),
            "password": password or faker.password(),
            "email": email or faker.email(),
        },
    )
