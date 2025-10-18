from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class TelegramWebhookMessage(BaseModel):
    """Schema for Telegram webhook message payload"""
    content: str
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    embeds: Optional[List[dict]] = None


class TelegramWebhookResponse(BaseModel):
    """Schema for Telegram webhook response"""
    message: str
    success: bool = True


# Telegram Bot API Schemas
class TelegramUser(BaseModel):
    """Telegram User schema"""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class TelegramChat(BaseModel):
    """Telegram Chat schema"""
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TelegramMessage(BaseModel):
    """Telegram Message schema"""
    message_id: int
    from_: Optional[TelegramUser] = None
    chat: TelegramChat
    date: int
    text: Optional[str] = None

    class Config:
        fields = {"from_": "from"}


class TelegramUpdate(BaseModel):
    """Telegram Update schema"""
    update_id: int
    message: Optional[TelegramMessage] = None


class SendMessageRequest(BaseModel):
    """Request schema for sending a message"""
    chat_id: int
    text: str
    parse_mode: Optional[str] = None
    reply_to_message_id: Optional[int] = None


class SendMessageResponse(BaseModel):
    """Response schema for sending a message"""
    ok: bool
    result: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
