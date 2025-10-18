from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TelegramUser(BaseModel):
    """Schema for Telegram user"""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class TelegramChat(BaseModel):
    """Schema for Telegram chat"""
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TelegramVoice(BaseModel):
    """Schema for Telegram voice message"""
    duration: int
    mime_type: str
    file_id: str
    file_unique_id: str
    file_size: int


class TelegramMessage(BaseModel):
    """Schema for Telegram message"""
    message_id: int
    from_: TelegramUser = Field(alias="from")
    chat: TelegramChat
    date: int
    text: Optional[str] = None
    voice: Optional[TelegramVoice] = None

    class Config:
        populate_by_name = True


class TelegramUpdate(BaseModel):
    """Schema for Telegram update/webhook payload"""
    update_id: int
    message: Optional[TelegramMessage] = None


class TelegramWebhookResponse(BaseModel):
    """Schema for Telegram webhook response"""
    message: str
    success: bool = True


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
