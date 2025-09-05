from typing import NoReturn
from uuid import UUID

from notes.exceptions import NoteNotFoundException
from shared.uows import SqlAlchemyUnitOfWork


async def update_note(
    uow: SqlAlchemyUnitOfWork,
    note_id: UUID,
    title: str | None = None,
    content: str | None = None,
) -> None | NoReturn:
    async with uow:
        note = await uow.notes.get_by_id(note_id, for_update=True)

        if not note:
            raise NoteNotFoundException()

        if note is not None:
            note.title = title

        if content is not None:
            note.content = content

        await uow.commit()
