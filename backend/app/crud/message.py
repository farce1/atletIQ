from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message_schemas import MessageCreate


def create_message(*, session: Session, message_in: MessageCreate) -> Message:
    db_message = Message(**message_in.model_dump())
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message
