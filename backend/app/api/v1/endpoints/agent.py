from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.api.deps import SessionsManagerDep
from app.api.exceptions.chat_exceptions import (
    session_not_found_error,
)
from app.schemas.agent.agent_query import BaseAgentQueryRequest, BaseAgentQueryResponse
from app.services.chat import ChatService

router = APIRouter()


@router.post("/query")
async def query_chat_agent(
    request: Request,
    agent_request: BaseAgentQueryRequest,
    sessions: SessionsManagerDep,
    chat_session_id: UUID,
    chat_service: ChatService = Depends(),
) -> BaseAgentQueryResponse:

    chat_agent_workflow = sessions.get_chat_session(chat_session_id)

    if chat_agent_workflow is None:
        raise session_not_found_error()

    response = await chat_service.process_query(
        agent_request.message, chat_session_id, chat_agent_workflow
    )

    return BaseAgentQueryResponse(response=response)
