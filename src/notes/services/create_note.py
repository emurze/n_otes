import logging
from uuid import UUID

from notes.models import Note
from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def create_note(
    uow: SqlAlchemyUnitOfWork,
    title: str,
    content: str,
    user_id: UUID,
) -> UUID:
    """Create a new note for a specific user."""
    logger.debug(
        "Creating note for user_id='%s' with title='%s'",
        user_id,
        title,
    )
    async with uow:
        note = Note(title=title, content=content, user_id=user_id)
        uow.notes.add(note)
        await uow.commit()

        logger.info(
            "Note created successfully with id='%s' for user_id='%s'",
            note.id,
            user_id,
        )
        return note.id
