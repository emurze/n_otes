import logging
from collections.abc import Callable
from typing import NoReturn
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import load_only

from notes.exceptions import NoteNotFoundException
from notes.models import Note
from notes.services.base import map_note_to_dto

logger = logging.getLogger(__name__)


async def get_note_by_id(
    session_factory: Callable,
    note_id: UUID,
) -> dict | NoReturn:
    """
    Retrieve a note by its unique identifier.
    Raises NoteNotFoundException if the note does not exist.
    """
    logger.debug("Fetching note with id='%s'", note_id)

    async with session_factory() as session:
        query = (
            select(Note)
            .where(Note.id == note_id)
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
        note = result.scalar_one_or_none()

        if not note:
            logger.warning("Note with id='%s' not found", note_id)
            raise NoteNotFoundException()

        note_dto = map_note_to_dto(note)
        logger.info("Note with id='%s' retrieved successfully", note_id)
        return note_dto
