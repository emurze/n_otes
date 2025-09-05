import logging
from typing import NoReturn
from uuid import UUID

from auth.exceptions import (
    TokenInvalidException,
    UserNotAuthenticatedException,
)
from auth.adapters.jwt_adapter import JWTAdapter
from auth.services.base import map_user_to_dto, map_user_to_tokens
from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def authenticate_user_by_access_token(
    jwt_adapter: JWTAdapter,
    uow: SqlAlchemyUnitOfWork,
    access_token: str,
    return_tokens: bool = True,
) -> dict | NoReturn:
    """
    Authenticate a user by validating an access token and returning either
    refreshed tokens or a user DTO.
    """
    logger.debug("Authenticating user with provided access token.")
    try:
        payload = jwt_adapter.get_access_token_payload(access_token)
        logger.debug(
            "Access token successfully decoded. Subject='%s'",
            payload.sub,
        )
    except TokenInvalidException as e:
        logger.warning("Token validation failed: %s", e.message)
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
            logger.warning(
                "Authentication failed: user with id=%s not found",
                payload.sub,
            )
            raise UserNotAuthenticatedException()

        logger.info("User '%s' authenticated successfully", user.username)

        if return_tokens:
            logger.debug(
                "Returning refreshed tokens for user '%s'",
                user.username,
            )
            return map_user_to_tokens(jwt_adapter, user)
        else:
            logger.debug("Returning DTO for user '%s'", user.username)
            return map_user_to_dto(user)
