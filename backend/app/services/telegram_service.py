import httpx
import logging
from typing import Optional

from app.core.config import settings
from app.schemas.telegram_schemas import SendMessageRequest, SendMessageResponse

logger = logging.getLogger(__name__)


class TelegramService:
    """Service for interacting with Telegram Bot API"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = settings.TELEGRAM_BOT_API_URL
        
        if not self.bot_token:
            logger.warning("TELEGRAM_BOT_TOKEN not configured")
    
    async def send_message(self, request: SendMessageRequest) -> SendMessageResponse:
        """
        Send a message via Telegram Bot API
        
        Args:
            request: SendMessageRequest with chat_id, text, and optional parameters
            
        Returns:
            SendMessageResponse with the result of the API call
        """
        if not self.bot_token:
            return SendMessageResponse(
                ok=False,
                description="Telegram bot token not configured"
            )
        
        url = f"{self.api_url}{self.bot_token.get_secret_value()}/sendMessage"
        
        payload = {
            "chat_id": request.chat_id,
            "text": request.text
        }
        
        if request.parse_mode:
            payload["parse_mode"] = request.parse_mode
            
        if request.reply_to_message_id:
            payload["reply_to_message_id"] = request.reply_to_message_id
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"Telegram API response: {result}")
                
                return SendMessageResponse(
                    ok=result.get("ok", False),
                    result=result.get("result"),
                    description=result.get("description")
                )
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error sending Telegram message: {str(e)}")
            return SendMessageResponse(
                ok=False,
                description=f"HTTP error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return SendMessageResponse(
                ok=False,
                description=f"Unexpected error: {str(e)}"
            )
    
    async def send_simple_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
        Convenience method to send a simple message
        
        Args:
            chat_id: Telegram chat ID
            text: Message text to send
            
        Returns:
            SendMessageResponse with the result
        """
        request = SendMessageRequest(chat_id=chat_id, text=text)
        return await self.send_message(request)
