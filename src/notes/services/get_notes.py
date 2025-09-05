import logging
from collections.abc import Callable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import load_only

from notes.models import Note
from notes.services.base import map_note_to_dto

logger = logging.getLogger(__name__)


async def get_user_notes(
    session_factory: Callable,
    user_id: UUID,
) -> list[dict]:
    """
    Retrieve all notes for a specific user.
    """
    logger.debug("Fetching all notes for user_id='%s'", user_id)

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
        notes = [map_note_to_dto(item) for item in result.scalars().all()]

    logger.info("Retrieved %d notes for user_id='%s'", len(notes), user_id)
    return notes
