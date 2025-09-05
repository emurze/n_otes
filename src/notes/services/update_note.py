import logging
from typing import NoReturn
from uuid import UUID

from notes.exceptions import NoteNotFoundException
from shared.uows import SqlAlchemyUnitOfWork

logger = logging.getLogger(__name__)


async def update_note(
    uow: SqlAlchemyUnitOfWork,
    note_id: UUID,
    title: str | None = None,
    content: str | None = None,
) -> None | NoReturn:
    """
    Update the title and/or content of an existing note.
    Only modifies fields that are provided in the parameters.
    """
    logger.debug("Attempting to update note with id='%s'", note_id)

    async with uow:
        note = await uow.notes.get_by_id(note_id, for_update=True)

        if not note:
            logger.warning("Note with id='%s' not found", note_id)
            raise NoteNotFoundException()

        if note is not None:
            note.title = title

        if content is not None:
            note.content = content

        await uow.commit()
        logger.info(
            "Note with id='%s' updated successfully. Updated fields: %s",
            note_id,
            {
                k: v
                for k, v in (("title", title), ("content", content))
                if v is not None
            },
        )
