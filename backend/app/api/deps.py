from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import db_session
from app.services.chat_manager import ChatSessionManager


def get_db() -> Generator[Session, None, None]:
    with db_session() as db:
        yield db


class ChatSessionManagerProvider:
    def __init__(self):
        self.chat_sessions_manager_instance = None

    def get_manager(self) -> ChatSessionManager:
        if self.chat_sessions_manager_instance is None:
            self.chat_sessions_manager_instance = ChatSessionManager()
        return self.chat_sessions_manager_instance


chat_agent_provider = ChatSessionManagerProvider()
get_sessions_manager = chat_agent_provider.get_manager

SessionsManagerDep = Annotated[ChatSessionManager, Depends(get_sessions_manager)]
SessionDep = Annotated[Session, Depends(get_db)]
