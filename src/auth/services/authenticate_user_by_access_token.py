from typing import NoReturn
from uuid import UUID

from auth.exceptions import (
    TokenInvalidException,
    UserNotAuthenticatedException,
)
from auth.adapters.jwt_adapter import JWTAdapter
from auth.services.base import map_user_to_dto, map_user_to_tokens
from shared.uows import SqlAlchemyUnitOfWork


async def authenticate_user_by_access_token(
    jwt_adapter: JWTAdapter,
    uow: SqlAlchemyUnitOfWork,
    access_token: str,
    return_tokens: bool = True,
) -> dict | NoReturn:
    try:
        payload = jwt_adapter.get_access_token_payload(access_token)
    except TokenInvalidException as e:
        raise UserNotAuthenticatedException(e.message)

    async with uow:
        user = await uow.users.get_by_id(
            UUID(payload.sub),
            load_fields=[
                "id",
                "name",
                "surname",
                "username",
                "phone_number",
                "email",
            ],
        )

        if user is None:
            raise UserNotAuthenticatedException()

        if return_tokens:
            return map_user_to_tokens(jwt_adapter, user)
        else:
            return map_user_to_dto(user)
