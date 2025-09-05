from enum import StrEnum
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from shared.db import Base


class Role(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    """Represents a user in the usecases."""
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    phone_number: Mapped[str | None]
    email: Mapped[str]
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum", create_constraint=True),
        default=Role.USER,
    )
    notes: Mapped[list["Note"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (f"{type(self).__name__}(username={self.username!r}, "
                f"role={self.role!r})")


class Note(Base):
    """Represents a note created by a user."""
    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(back_populates="notes")

    def __repr__(self) -> str:
        return (f"{type(self).__name__}(title={self.title!r}, "
                f"created_at={self.created_at!r})")
