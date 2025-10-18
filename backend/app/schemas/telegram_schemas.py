from pydantic import BaseModel
from typing import Optional, List


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
