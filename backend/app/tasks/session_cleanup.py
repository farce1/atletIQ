import logging
from datetime import datetime, timedelta, timezone

from celery import shared_task
from sqlalchemy import delete, select, update

from app.api.deps import chat_agent_provider
from app.db import db_session
from app.models.chat_session import ChatSession

log = logging.getLogger(__name__)


@shared_task
def mark_inactive_sessions():
    log.info("Task mark_inactive_sessions started.")

    with db_session() as db:
        inactive_threshold = datetime.now(timezone.utc) - timedelta(hours=1)

        stmt = (
            update(ChatSession)
            .where(ChatSession.active.is_(True))
            .where(ChatSession.updated_at < inactive_threshold)
            .values(active=False)
        )

        result = db.execute(stmt)

        log.info(f"Marked {result.rowcount} sessions as inactive.")

    log.info("Task mark_inactive_sessions finished.")


@shared_task
def cleanup_inactive_sessions():
    log.info("Task cleanup_inactive_sessions started.")

    chat_session_manager = chat_agent_provider.get_manager()

    with db_session() as db:
        stmt_select = select(ChatSession).where(ChatSession.active.is_(False))

        select_result = db.execute(stmt_select).scalars().all()

        inactive_session_ids = [session.id for session in select_result]

        log.info(
            f"Found {len(inactive_session_ids)} inactive sessions in the database."
        )

        removed_sessions = []

        for session_id in inactive_session_ids:
            if chat_session_manager.get_chat_session(session_id):
                chat_session_manager.delete_chat_session(session_id)
                removed_sessions.append(str(session_id))

        if removed_sessions:
            log.info(
                f"Deleted {len(removed_sessions)} sessions from ChatSessionManager."
            )
        else:
            log.info("No sessions removed from ChatSessionManager.")

        stmt_delete = delete(ChatSession).where(
            ChatSession.id.in_(inactive_session_ids)
        )
        result = db.execute(stmt_delete)

        log.info(f"Deleted {result.rowcount} inactive sessions from the database.")

    log.info("Task cleanup_inactive_sessions finished.")
