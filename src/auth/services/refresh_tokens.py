import logging
from typing import Any, NoReturn
from uuid import UUID

from auth.adapters.jwt_adapter import JWTAdapter
from auth.exceptions import (
    TokenInvalidException,
    UserNotAuthenticatedException,
)
from auth.services.base import map_user_to_tokens
from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def refresh_tokens(
    refresh_token: str,
    uow: SqlAlchemyUnitOfWork,
    jwt_adapter: JWTAdapter,
) -> dict | NoReturn:
    """Refreshes the access and refresh tokens."""
    try:
        payload = jwt_adapter.get_refresh_token_payload(refresh_token)
    except TokenInvalidException as e:
        raise UserNotAuthenticatedException(e.message)

    async with uow:
        user: Any = await uow.users.get_by_id(UUID(payload.sub))

        if not user:
            raise UserNotAuthenticatedException()

        return map_user_to_tokens(jwt_adapter, user)
