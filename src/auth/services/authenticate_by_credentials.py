import logging
from typing import NoReturn

from auth.adapters.jwt_adapter import JWTAdapter
from auth.adapters.password_hash_adapter import PasswordHashAdapter
from auth.exceptions import UserNotAuthenticatedException
from auth.services.base import map_user_to_tokens
from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def authenticate_user_by_credentials(
    username: str,
    password: str,
    uow: SqlAlchemyUnitOfWork,
    ph: PasswordHashAdapter,
    jwt_adapter: JWTAdapter,
) -> dict | NoReturn:
    """
    Authenticate a user by validating their username and password.
    Returns JWT tokens if successful, otherwise raises an authentication error.
    """
    logger.debug("Attempting authentication for username='%s'", username)

    async with uow:
        user = await uow.users.get_by_username(
            username,
            load_fields=[
                "id",
                "username",
                "email",
                "password",
            ],
        )

        if not user:
            logger.warning(
                "Authentication failed: user '%s' not found",
                username,
            )
            raise UserNotAuthenticatedException(
                "Incorrect username or password"
            )

        if not user.verify_password(password, ph=ph):
            logger.warning(
                "Authentication failed: invalid password for user '%s'",
                username,
            )
            raise UserNotAuthenticatedException(
                "Incorrect username or password"
            )

        tokens = map_user_to_tokens(jwt_adapter, user)
        logger.info("User '%s' authenticated successfully", username)
        return tokens
