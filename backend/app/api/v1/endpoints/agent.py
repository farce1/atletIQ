from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.api.deps import SessionsManagerDep
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
    """Query the Claude agent with non-streaming response by default."""

    response = await chat_service.process_query(agent_request.message, chat_session_id)

    return BaseAgentQueryResponse(response=response)
