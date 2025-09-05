from collections.abc import Callable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import load_only

from notes.models import Note
from notes.services.base import map_note_to_dto


async def get_user_notes(
    session_factory: Callable,
    user_id: UUID,
) -> list[dict]:
    async with session_factory() as session:
        query = (
            select(Note)
            .where(Note.user_id == user_id)
            .options(
                load_only(
                    Note.id,
                    Note.title,
                    Note.content,
                    Note.user_id,
                )
            )
        )
        result = await session.execute(query)
        return [map_note_to_dto(item) for item in result.scalars().all()]
