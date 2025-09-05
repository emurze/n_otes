from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from shared.db import Base

if TYPE_CHECKING:
    from auth.models import User  # type: ignore


class Note(Base):
    """Represents a note created by a user."""

    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(back_populates="notes")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(title={self.title!r})"
