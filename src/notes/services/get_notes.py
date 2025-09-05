from collections.abc import Callable
from uuid import UUID

from sqlalchemy import select

from notes.models import Note


async def get_user_notes(
    session_factory: Callable,
    user_id: UUID,
) -> list[Note]:
    async with session_factory() as session:
        query = select(Note).where(Note.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()
