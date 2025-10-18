from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import ChatSession


def create_chat_session(*, session: Session) -> ChatSession:
    db_obj = ChatSession()
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete_chat_session(*, session: Session, chat_session_id: UUID) -> None:
    session.query(ChatSession).filter(ChatSession.id == chat_session_id).delete()
    session.commit()
    return None


def update_chat_session(session: Session, chat_session: ChatSession):
    chat_session.updated_at = func.now()
    session.commit()
    session.refresh(chat_session)
    return chat_session
