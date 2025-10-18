from uuid import UUID

from pydantic import BaseModel

from app.schemas.agent.message_roles import MessageRole


class MessageBase(BaseModel):
    conversation_id: UUID
    role: MessageRole
    content: str


class MessageCreate(MessageBase):
    pass
