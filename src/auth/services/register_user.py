from typing import NoReturn
from uuid import UUID

from auth.adapters.password_hash_adapter import PasswordHashAdapter
from auth.exceptions import UserConflictException
from auth.models import User
from shared.uows import SqlAlchemyUnitOfWork


async def register_user(
    ph: PasswordHashAdapter,
    uow: SqlAlchemyUnitOfWork,
    name: str,
    surname: str,
    username: str,
    password: str,
    email: str,
) -> NoReturn | UUID:
    """Handler function for signing up a user."""
    async with uow:
        if await uow.users.check_by_username(username):
            raise UserConflictException("Username already exists")

        if await uow.users.check_by_email(str(email)):
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
        return user.id
