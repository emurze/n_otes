from typing import NoReturn

from auth.adapters.jwt_adapter import JWTAdapter
from auth.adapters.password_hash_adapter import PasswordHashAdapter
from auth.exceptions import UserNotAuthenticatedException
from auth.services.base import map_user_to_tokens
from shared.uows import SqlAlchemyUnitOfWork


async def authenticate_user_by_credentials(
    username: str,
    password: str,
    uow: SqlAlchemyUnitOfWork,
    ph: PasswordHashAdapter,
    jwt_adapter: JWTAdapter,
) -> dict | NoReturn:
    async with uow:
        user = await uow.users.get_by_username(username)

        if not user:
            raise UserNotAuthenticatedException(
                "Incorrect username or password"
            )

        if not user.verify_password(password, ph=ph):
            raise UserNotAuthenticatedException(
                "Incorrect username or password"
            )

        return map_user_to_tokens(jwt_adapter, user)
