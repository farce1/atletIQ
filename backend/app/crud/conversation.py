from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Conversation


def create_conversation(
    *, session: Session, session_id: Optional[UUID] = None
) -> Conversation:
    db_conversation = Conversation()
    db_conversation.session_id = session_id
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation


def get_conversation_by_session_id(
    *, session: Session, session_id: UUID
) -> Optional[Conversation]:
    statement = select(Conversation).where(Conversation.session_id == session_id)
    conversation = session.execute(statement).scalars().first()
    return conversation
