from io import BytesIO
from typing import BinaryIO
import httpx
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self) -> None:
        if not settings.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not configured in settings")
        self.token = settings.TELEGRAM_BOT_TOKEN.get_secret_value()
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def get_file_path(self, file_id: str) -> str:
        """
        Get the file path for a Telegram file using its file_id.

        Args:
            file_id: The Telegram file ID

        Returns:
            str: The file path on Telegram servers
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/getFile", params={"file_id": file_id})
            response.raise_for_status()
            data = response.json()

            if not data.get("ok"):
                raise ValueError(f"Failed to get file path: {data.get('description')}")

            return data["result"]["file_path"]

    async def download_file(self, file_path: str) -> BinaryIO:
        """
        Download a file from Telegram servers.

        Args:
            file_path: The file path on Telegram servers

        Returns:
            BinaryIO: File content as a binary stream
        """
        file_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"

        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            response.raise_for_status()

            # Create a BytesIO buffer with the file content
            file_buffer = BytesIO(response.content)
            file_buffer.seek(0)

            return file_buffer

    async def download_voice_message(self, file_id: str) -> BinaryIO:
        """
        Download a voice message from Telegram.

        Args:
            file_id: The Telegram voice file ID

        Returns:
            BinaryIO: Voice file content as a binary stream
        """
        logger.info(f"Downloading voice message with file_id: {file_id}")
        file_path = await self.get_file_path(file_id)
        logger.info(f"Got file path: {file_path}")
        return await self.download_file(file_path)

    async def send_text_message(self, chat_id: int, text: str) -> dict:
        """
        Send a text message to a Telegram chat.

        Args:
            chat_id: The Telegram chat ID
            text: The message text

        Returns:
            dict: Telegram API response
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sendMessage",
                json={"chat_id": chat_id, "text": text}
            )
            response.raise_for_status()
            return response.json()

    async def send_voice_message(self, chat_id: int, voice_file: BinaryIO) -> dict:
        """
        Send a voice message to a Telegram chat.

        Args:
            chat_id: The Telegram chat ID
            voice_file: The voice file as a binary stream

        Returns:
            dict: Telegram API response
        """
        async with httpx.AsyncClient() as client:
            files = {"voice": ("voice.ogg", voice_file, "audio/ogg")}
            data = {"chat_id": str(chat_id)}

            response = await client.post(
                f"{self.base_url}/sendVoice",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
