from typing import Optional
from uuid import UUID

from app.schemas.agent.agent_modes import AgentModes
from app.schemas.languages import Languages


class ChatSessionManager:
    def __init__(self):
        self.chat_sessions: dict[UUID] = {}

    def create_chat_session(
        self,
        chat_session_id: UUID,
        chat_language: Languages,
        chat_agent_mode: AgentModes,
    ) -> UUID:
        """
        Create a new chat session and initialize its workflow.
        """

        self.chat_sessions[chat_session_id] = None  # type: ignore[assignment]

        return chat_session_id

    def get_chat_session(self, chat_session_id: UUID) -> Optional[str]:
        """
        Get an existing chat session.
        """
        return self.chat_sessions.get(chat_session_id)

    def delete_chat_session(self, chat_session_id: UUID) -> None:
        """
        Delete an existing chat session.
        """
        if chat_session_id in self.chat_sessions:
            del self.chat_sessions[chat_session_id]

    def list_active_sessions(self) -> list[UUID]:
        """
        List all active chat session IDs.
        """
        return list(self.chat_sessions.keys())
