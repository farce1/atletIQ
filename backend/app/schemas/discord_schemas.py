from pydantic import BaseModel
from typing import Optional, List


class DiscordWebhookMessage(BaseModel):
    """Schema for Discord webhook message payload"""
    content: str
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    embeds: Optional[List[dict]] = None


class DiscordWebhookResponse(BaseModel):
    """Schema for Discord webhook response"""
    message: str
    success: bool = True
