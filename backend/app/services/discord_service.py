import httpx
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class DiscordService:
    """Service for interacting with Discord API"""
    
    def __init__(self):
        self.base_url = settings.DISCORD_API_BASE_URL
        self.bot_token = settings.DISCORD_BOT_TOKEN.get_secret_value() if settings.DISCORD_BOT_TOKEN else None
        
        if not self.bot_token:
            logger.warning("Discord bot token not configured. Discord API calls will fail.")
    
    async def send_message(
        self, 
        channel_id: str, 
        content: str, 
        embeds: Optional[list[Dict[str, Any]]] = None,
        components: Optional[list[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to a Discord channel using the Discord API.
        
        Args:
            channel_id: The Discord channel ID to send the message to
            content: The message content
            embeds: Optional list of embed objects
            components: Optional list of component objects (buttons, select menus, etc.)
            
        Returns:
            Dict containing the Discord API response
            
        Raises:
            httpx.HTTPError: If the API request fails
            ValueError: If bot token is not configured
        """
        if not self.bot_token:
            raise ValueError("Discord bot token not configured")
        
        url = f"{self.base_url}/channels/{channel_id}/messages"
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "content": content
        }
        
        if embeds:
            payload["embeds"] = embeds
            
        if components:
            payload["components"] = components
        
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Sending Discord message to channel {channel_id}")
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"Successfully sent Discord message. Message ID: {result.get('id')}")
                return result
                
            except httpx.HTTPError as e:
                logger.error(f"Failed to send Discord message: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Discord API error response: {e.response.text}")
                raise
    
    async def send_direct_message(
        self, 
        user_id: str, 
        content: str, 
        embeds: Optional[list[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send a direct message to a Discord user.
        
        Args:
            user_id: The Discord user ID to send the message to
            content: The message content
            embeds: Optional list of embed objects
            
        Returns:
            Dict containing the Discord API response
            
        Raises:
            httpx.HTTPError: If the API request fails
            ValueError: If bot token is not configured
        """
        if not self.bot_token:
            raise ValueError("Discord bot token not configured")
        
        # First, create a DM channel with the user
        url = f"{self.base_url}/users/@me/channels"
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "recipient_id": user_id
        }
        
        async with httpx.AsyncClient() as client:
            try:
                # Create DM channel
                logger.info(f"Creating DM channel with user {user_id}")
                dm_response = await client.post(url, json=payload, headers=headers)
                dm_response.raise_for_status()
                dm_channel = dm_response.json()
                
                # Send message to the DM channel
                return await self.send_message(
                    channel_id=dm_channel["id"],
                    content=content,
                    embeds=embeds
                )
                
            except httpx.HTTPError as e:
                logger.error(f"Failed to send Discord DM: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Discord API error response: {e.response.text}")
                raise
    
    async def edit_message(
        self, 
        channel_id: str, 
        message_id: str, 
        content: str, 
        embeds: Optional[list[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Edit an existing Discord message.
        
        Args:
            channel_id: The Discord channel ID where the message is located
            message_id: The ID of the message to edit
            content: The new message content
            embeds: Optional list of embed objects
            
        Returns:
            Dict containing the Discord API response
            
        Raises:
            httpx.HTTPError: If the API request fails
            ValueError: If bot token is not configured
        """
        if not self.bot_token:
            raise ValueError("Discord bot token not configured")
        
        url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "content": content
        }
        
        if embeds:
            payload["embeds"] = embeds
        
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Editing Discord message {message_id} in channel {channel_id}")
                response = await client.patch(url, json=payload, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"Successfully edited Discord message {message_id}")
                return result
                
            except httpx.HTTPError as e:
                logger.error(f"Failed to edit Discord message: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Discord API error response: {e.response.text}")
                raise


# Create a singleton instance
discord_service = DiscordService()
