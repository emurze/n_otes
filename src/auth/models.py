from typing import Any, Self, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from auth.adapters.password_hash_adapter import PasswordHashAdapter
from shared.db import Base

if TYPE_CHECKING:
    from notes.models import Note  # type: ignore


class User(Base):
    """Represents a user in the use cases."""

    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    username: Mapped[str] = mapped_column(index=True)
    password: Mapped[str]
    phone_number: Mapped[str | None]
    email: Mapped[str] = mapped_column(index=True)
    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @classmethod
    def create(
        cls,
        password: str,
        *,
        ph: PasswordHashAdapter,
        **kw: Any,
    ) -> Self:
        """
        Factory method to instantiate a User with a securely hashed password.
        """
        return cls(**kw, password=ph.hash_password(password))

    def verify_password(
        self,
        password: str,
        *,
        ph: PasswordHashAdapter,
    ) -> bool:
        """Verify a plain-text password against the stored hashed password."""
        return ph.verify_password(password, self.password)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(username={self.username!r}"
