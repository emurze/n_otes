from collections.abc import Callable
from typing import NoReturn
from uuid import UUID

from sqlalchemy import select

from notes.exceptions import NoteNotFoundException
from notes.models import Note
from notes.services.base import map_note_to_dto


async def get_note_by_id(
    session_factory: Callable,
    note_id: UUID,
) -> dict | NoReturn:
    async with session_factory() as session:
        query = select(Note).where(Note.id == note_id)
        result = await session.execute(query)
        note = result.scalar_one_or_none()

        if not note:
            raise NoteNotFoundException()

        return map_note_to_dto(note)
