from fastapi import APIRouter

from app.api.v1.endpoints import agent, telegram

api_router = APIRouter()
api_router.include_router(
    agent.router,
    prefix="/agent",
    tags=["agent"],
)
api_router.include_router(
    telegram.router,
    prefix="/telegram",
    tags=["telegram"],
)
