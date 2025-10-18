from fastapi import APIRouter

from app.api.v1.endpoints import agent, chat, discord

api_router = APIRouter()
api_router.include_router(
    agent.router,
    prefix="/agent",
    tags=["agent"],
)
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"],
)
api_router.include_router(
    discord.router,
    prefix="/discord",
    tags=["discord"],
)
