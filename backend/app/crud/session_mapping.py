from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SessionMapping


def create_session_mapping(
    *, session: Session, external_id: str, session_uuid: UUID
) -> SessionMapping:
    """Create a new session mapping."""
    db_mapping = SessionMapping(external_id=external_id, session_uuid=session_uuid)
    session.add(db_mapping)
    session.commit()
    session.refresh(db_mapping)
    return db_mapping


def get_session_mapping_by_external_id(
    *, session: Session, external_id: str
) -> Optional[SessionMapping]:
    """Get session mapping by external ID."""
    statement = select(SessionMapping).where(SessionMapping.external_id == external_id)
    mapping = session.execute(statement).scalars().first()
    return mapping


def get_session_uuid_by_external_id(
    *, session: Session, external_id: str
) -> Optional[UUID]:
    """Get session UUID by external ID."""
    mapping = get_session_mapping_by_external_id(
        session=session, external_id=external_id
    )
    return mapping.session_uuid if mapping else None


def delete_session_mapping(*, session: Session, external_id: str) -> bool:
    """Delete session mapping by external ID."""
    mapping = get_session_mapping_by_external_id(
        session=session, external_id=external_id
    )
    if mapping:
        session.delete(mapping)
        session.commit()
        return True
    return False
