from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class SqlAlchemyGenericRepository(Generic[T]):
    """Generic repository for basic CRUD operations."""

    def __init__(self, session: AsyncSession, model_class: Type[T]) -> None:
        self._session = session
        self.model_class = model_class

    def add(self, entity: T) -> None:
        """Add a new entity to the session."""
        self._session.add(entity)

    async def get_by_id(self, entity_id) -> T | None:
        """Retrieve an entity by its primary key."""
        result = await self._session.execute(
            select(self.model_class).filter_by(id=entity_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, entity: T) -> None:
        """Delete an entity."""
        await self._session.delete(entity)
