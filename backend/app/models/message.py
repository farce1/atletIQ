from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.schemas.agent.message_roles import MessageRole

if TYPE_CHECKING:
    from app.models import Conversation


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=func.uuid_generate_v4(),
        index=True,
    )
    conversation_id: Mapped[PythonUUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")
