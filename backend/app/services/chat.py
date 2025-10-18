from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from app.agent.engines.core_agent import get_claude_agent, ClaudeAgentError
from app.api.deps import get_db
from app.core.config import get_settings
from app.api.exceptions.chat_exceptions import conversation_not_found_error
from app.crud.chat import create_chat_session
from app.crud.conversation import create_conversation, get_conversation_by_session_id
from app.crud.message import create_message
from app.models import ChatSession, Conversation
from app.schemas.agent.message_roles import MessageRole
from app.schemas.message_schemas import MessageCreate


class ChatService:
    def __init__(self, db: Session = Depends(get_db)):
        self._db = db
        self._settings = get_settings()

    def create_chat_session(self) -> UUID:
        try:
            chat_session = create_chat_session(session=self._db)
            session_id = chat_session.id
        except Exception:
            self._db.rollback()
            raise
        return session_id

    def get_chat_session_by_session_id(self, session_id: UUID) -> Optional[ChatSession]:
        statement = select(ChatSession).where(ChatSession.id == session_id)
        chat_session = self._db.execute(statement).scalars().first()
        return chat_session

    def delete_chat_session(self, db_obj: ChatSession):
        self._db.delete(db_obj)
        self._db.commit()

    def create_conversation(self, session_id: UUID | None) -> Conversation:
        try:
            conversation = create_conversation(session=self._db, session_id=session_id)
            return conversation
        except Exception:
            self._db.rollback()
            raise

    def add_message(
        self,
        session_id: UUID,
        content: str,
        role: MessageRole,
    ) -> None:
        try:
            conversation = get_conversation_by_session_id(
                session=self._db, session_id=session_id
            )

            if conversation is None:
                raise conversation_not_found_error()

            message = MessageCreate(
                conversation_id=conversation.id, role=role, content=content
            )
            create_message(session=self._db, message_in=message)
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise

    async def process_query(
        self,
        message: str,
        chat_session_id: UUID,
    ) -> str:
        """Process a query using the Claude agent."""
        try:
            # Add user message to database
            self.add_message(chat_session_id, message, MessageRole.USER)

            # Get Claude agent and process the message
            claude_agent = get_claude_agent()
            response_text = await claude_agent.process_message(
                session_id=chat_session_id,
                message=message,
                stream=self._settings.CLAUDE_AGENT_ENABLE_STREAMING,
            )

            # Add assistant response to database
            self.add_message(chat_session_id, response_text, role=MessageRole.ASSISTANT)

            return response_text

        except ClaudeAgentError as e:
            # Log the error and return a fallback response
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            self.add_message(chat_session_id, error_message, role=MessageRole.ASSISTANT)
            return error_message
        except Exception:
            # Log unexpected errors and return a generic error message
            error_message = (
                "I apologize, but I encountered an unexpected error. Please try again."
            )
            self.add_message(chat_session_id, error_message, role=MessageRole.ASSISTANT)
            return error_message
