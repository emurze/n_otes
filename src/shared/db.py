import re
import uuid
from datetime import datetime

from sqlalchemy import MetaData, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from shared.identity_provider import provide_identity


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        """Convert CamelCase to snake_case"""
        return (
            re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__)
            .lower()
            .rstrip("_model")
        )

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_"
                  "%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=provide_identity,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
    )
