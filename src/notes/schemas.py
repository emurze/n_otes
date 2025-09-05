from pydantic import BaseModel
from uuid import UUID


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteRead(BaseModel):
    id: UUID
    title: str
    content: str
    user_id: UUID
