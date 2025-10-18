from sqlalchemy.orm import Session

from app.models.dummy import DummyLog
from app.schemas.dummy_schemas import DummyLogCreate


def create_dummy_log(*, session: Session, dummy_log_in: DummyLogCreate) -> DummyLog:
    db_message = DummyLog(**dummy_log_in.model_dump())
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message
