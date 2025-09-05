from typing import Generic, TypeVar, Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import load_only

from auth.models import User

T = TypeVar("T")


class SqlAlchemyGenericRepository(Generic[T]):
    """Generic repository for basic CRUD operations."""

    def __init__(self, session: AsyncSession, model_class: Type[T]) -> None:
        self._session = session
        self.model_class = model_class

    def add(self, model: T) -> None:
        """Add a new model to the session."""
        self._session.add(model)

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
        load_fields: list | None = None,
    ) -> T | None:
        """Retrieve a model by its primary key."""
        query = select(self.model_class).filter_by(id=entity_id)

        if load_fields:
            query = query.options(
                load_only(*[getattr(User, field) for field in load_fields])
            )

        if for_update:
            query = query.with_for_update()

        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, model: T) -> None:
        """Delete a model."""
        await self._session.delete(model)
