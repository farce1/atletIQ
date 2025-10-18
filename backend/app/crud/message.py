from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message_schemas import MessageCreate


def create_message(*, session: Session, message_in: MessageCreate) -> Message:
    db_message = Message(**message_in.model_dump())
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def get_messages_by_conversation_id(
    *, session: Session, conversation_id: UUID
) -> List[Message]:
    """Get all messages for a conversation, ordered by timestamp."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp)
    )
    messages = session.execute(statement).scalars().all()
    return list(messages)
