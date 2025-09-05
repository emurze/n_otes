import logging
from uuid import UUID

from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def delete_note(uow: SqlAlchemyUnitOfWork, note_id: UUID) -> None:
    """Delete a note by its unique identifier."""
    logger.debug("Attempting to delete note with id='%s'", note_id)

    async with uow:
        note = await uow.notes.get_by_id(note_id)

        if note is not None:
            await uow.notes.delete(note)
            await uow.commit()
            logger.info("Note with id='%s' deleted successfully", note_id)
        else:
            logger.warning(
                "Note with id='%s' not found; nothing to delete", note_id
            )
