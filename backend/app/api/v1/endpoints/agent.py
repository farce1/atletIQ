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
    chat_id: str,
    chat_service: ChatService = Depends(),
) -> BaseAgentQueryResponse:
    response = await chat_service.process_query(agent_request.message, chat_id)

    return BaseAgentQueryResponse(response=response)
