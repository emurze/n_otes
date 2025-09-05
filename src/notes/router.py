from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from starlette import status

from auth.dependencies import get_current_user
from auth.schemas import UserRead
from notes import services
from notes.exceptions import NoteNotFoundException
from shared.dependencies import get_uow, get_session_factory
from shared.schemas import ErrorSchema
from shared.uows import SqlAlchemyUnitOfWork
from notes.schemas import NoteCreate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post(
    "/",
    response_model=NoteRead,
    summary="Create a new note",
    description="Create a new note for the current authenticated user "
    "and return the created note.",
)
async def create_note(
    note_in: NoteCreate,
    current_user: UserRead = Depends(get_current_user),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    session_factory: Callable = Depends(get_session_factory),
):
    note_id = await services.create_note(
        uow=uow,
        title=note_in.title,
        content=note_in.content,
        user_id=current_user.id,
    )
    return await services.get_note_by_id(session_factory, note_id)


@router.get(
    "/",
    response_model=list[NoteRead],
    summary="List all notes of the current user",
    description="Return all notes that belong to the authenticated user.",
)
async def get_notes(
    current_user: UserRead = Depends(get_current_user),
    session_factory: Callable = Depends(get_session_factory),
):
    return await services.get_user_notes(session_factory, current_user.id)


@router.get(
    "/{note_id}",
    response_model=NoteRead,
    summary="Get a note by ID",
    description="Retrieve a specific note by its ID. ",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
    dependencies=[Depends(get_current_user)],
)
async def get_note_by_id(
    note_id: UUID,
    session_factory: Callable = Depends(get_session_factory),
):
    try:
        return await services.get_note_by_id(session_factory, note_id)
    except NoteNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_note_endpoint(
    note_id: UUID,
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
):
    await services.delete_note(uow, note_id)
