from uuid import UUID

from shared.uows import SqlAlchemyUnitOfWork


async def delete_note(uow: SqlAlchemyUnitOfWork, note_id: UUID) -> None:
    async with uow:
        note = await uow.notes.get_by_id(note_id)
        if note is not None:
            await uow.notes.delete(note)
            await uow.commit()
