from datetime import datetime
from typing import Optional
from uuid import UUID

from shared.schemas import Schema


class TokenRead(Schema):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserSignup(Schema):
    name: str
    surname: str
    username: str
    password: str
    email: str


class UserRead(Schema):
    id: Optional[UUID] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
