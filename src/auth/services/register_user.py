import logging
from typing import NoReturn
from uuid import UUID

from auth.adapters.password_hash_adapter import PasswordHashAdapter
from auth.exceptions import UserConflictException
from auth.models import User
from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def register_user(
    ph: PasswordHashAdapter,
    uow: SqlAlchemyUnitOfWork,
    name: str,
    surname: str,
    username: str,
    password: str,
    email: str,
) -> NoReturn | UUID:
    """Register a new user in the system."""
    logger.debug(
        "Attempting to register user with username='%s', email='%s'",
        username,
        email,
    )
    async with uow:
        if await uow.users.check_by_username(username):
            logger.warning(
                "Registration failed: username '%s' already exists",
                username,
            )
            raise UserConflictException("Username already exists")

        if await uow.users.check_by_email(str(email)):
            logger.warning(
                "Registration failed: email '%s' already exists",
                email,
            )
            raise UserConflictException("Email already exists")

        user = User.create(
            name=name,
            surname=surname,
            username=username,
            password=password,
            email=email,
            ph=ph,
        )
        uow.users.add(user)
        await uow.commit()

        logger.info(
            "User registered successfully with id='%s', username='%s'",
            user.id,
            username,
        )
        return user.id
