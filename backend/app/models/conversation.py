from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID as PythonUUID

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models import ChatSession, Message


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=func.uuid_generate_v4(),
        index=True,
    )
    session_id: Mapped[Optional[PythonUUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    session: Mapped[Optional["ChatSession"]] = relationship(
        back_populates="conversation"
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )
