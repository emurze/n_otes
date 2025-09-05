from collections.abc import Callable
from typing import Self

from auth.models import User
from auth.adapters.user_repository import UserSqlAlchemyRepository
from notes.models import Note
from shared.repositories import SqlAlchemyGenericRepository


class SqlAlchemyUnitOfWork:
    users: UserSqlAlchemyRepository

    def __init__(self, session_factory: Callable) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self.users = UserSqlAlchemyRepository(self.session, User)
        self.notes = SqlAlchemyGenericRepository(self.session, Note)
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
