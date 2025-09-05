from typing import Any, Self

from sqlalchemy.orm import Mapped

from auth.adapters.password_hash_adapter import PasswordHashAdapter
from shared.db import Base


class User(Base):
    """Represents a user in the usecases."""

    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    phone_number: Mapped[str | None]
    email: Mapped[str]

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
        return ph.verify_password(password, self.password)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(username={self.username!r}"
