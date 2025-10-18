from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query

from app.api.deps import SessionsManagerDep
from app.api.exceptions.chat_exceptions import (
    session_not_found_error,
)
from app.schemas.agent.agent_modes import AgentModes
from app.schemas.chat_schemas import CreateChatSessionResponse
from app.schemas.languages import Languages
from app.services.chat import ChatService

router = APIRouter()


@router.post("/")
async def create_session(
    sessions: SessionsManagerDep,
    language: Languages = Query(Languages.EN, description="Coversation base language"),
    agent: AgentModes = Query(AgentModes.GENERAL, description="The agent to query"),
    chat_sessions_service: ChatService = Depends(),
) -> CreateChatSessionResponse:
    chat_session_id = chat_sessions_service.create_chat_session()
    chat_session_id = sessions.create_chat_session(chat_session_id, language, agent)
    conversation = chat_sessions_service.create_conversation(chat_session_id)

    return CreateChatSessionResponse(
        conversation_id=conversation.id, session_id=conversation.session_id
    )


@router.delete("/{chat_session_id}")
async def delete_session(
    sessions: SessionsManagerDep,
    chat_session_id: UUID = Path(
        ..., description="The ID of the chat session to delete"
    ),
    chat_sessions_service: ChatService = Depends(),
) -> None:
    chat_session = chat_sessions_service.get_chat_session_by_session_id(chat_session_id)

    if chat_session is None:
        raise session_not_found_error()

    sessions.delete_chat_session(chat_session.id)
    chat_sessions_service.delete_chat_session(chat_session)
