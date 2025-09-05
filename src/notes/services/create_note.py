from uuid import UUID

from notes.models import Note
from shared.uows import SqlAlchemyUnitOfWork


async def create_note(
    uow: SqlAlchemyUnitOfWork,
    title: str,
    content: str,
    user_id: UUID,
) -> UUID:
    async with uow:
        note = Note(title=title, content=content, user_id=user_id)
        uow.notes.add(note)
        await uow.commit()
        return note.id
