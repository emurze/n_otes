import logging
from typing import NoReturn
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
    """Refreshes the access and refresh tokens for a valid user."""
    logger.debug(
        "Attempting to refresh tokens using refresh_token='%s...'",
        refresh_token[:10],
    )
    try:
        payload = jwt_adapter.get_refresh_token_payload(refresh_token)
        logger.debug(
            "Refresh token decoded successfully for user_id='%s'",
            payload.sub,
        )
    except TokenInvalidException as e:
        logger.warning("Invalid refresh token provided: %s", e.message)
        raise UserNotAuthenticatedException(e.message)

    async with uow:
        user = await uow.users.get_by_id(
            UUID(payload.sub),
            load_fields=[
                "id",
                "username",
                "email",
            ],
        )

        if not user:
            logger.warning(
                "Token refresh failed: user with id='%s' not found",
                payload.sub,
            )
            raise UserNotAuthenticatedException()

        logger.info("Tokens refreshed successfully for user_id='%s'", user.id)
        return map_user_to_tokens(jwt_adapter, user)
