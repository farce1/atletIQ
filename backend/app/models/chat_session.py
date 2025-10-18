from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Conversation


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=func.uuid_generate_v4(),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(back_populates="session")
