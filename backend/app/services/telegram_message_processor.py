from typing import BinaryIO
import logging
from sqlalchemy.orm import Session

from app.services.telegram_service import TelegramService
from app.services.tts_service import TextToSpeechService
from app.services.chat import ChatService

logger = logging.getLogger(__name__)


class TelegramMessageProcessor:
    """Processes Telegram messages and generates responses."""

    def __init__(self, db: Session):
        self.db = db
        self.chat_service = ChatService(db=db)

    def get_session_id(self, chat_id: int) -> str:
        """Generate a unique session ID for a Telegram chat."""
        return f"telegram_{chat_id}"

    async def process_query(self, message: str, chat_id: int) -> str:
        """
        Process user query through chat service and get AI response.

        Args:
            message: User message text
            chat_id: Telegram chat ID

        Returns:
            str: AI response text
        """
        session_id = self.get_session_id(chat_id)
        logger.info(f"Processing query for session {session_id}: {message}")

        # For now, always respond with "Hello World" in English
        response_text = "Hello World"

        logger.info(f"Generated response: {response_text}")
        return response_text


class VoiceMessageProcessor:
    """Handles voice message transcription and voice response generation."""

    def __init__(self):
        self.telegram_service = TelegramService()
        self.tts_service = TextToSpeechService()

    async def download_and_transcribe(self, file_id: str) -> str:
        """
        Download voice message from Telegram and transcribe it to text.

        Args:
            file_id: Telegram file ID

        Returns:
            str: Transcribed text
        """
        logger.info(f"Downloading voice message with file_id: {file_id}")
        voice_file = await self.telegram_service.download_voice_message(file_id)

        logger.info("Transcribing voice to text")
        transcribed_text = await self.tts_service.convert_speech_to_text(voice_file)
        logger.info(f"Transcribed text: {transcribed_text}")

        return transcribed_text

    async def convert_and_send_voice(self, chat_id: int, text: str) -> None:
        """
        Convert text to speech and send as voice message.

        Args:
            chat_id: Telegram chat ID
            text: Text to convert to speech
        """
        logger.info("Converting response to speech")
        response_audio = await self.tts_service.convert_text_to_speech(text)

        logger.info(f"Sending voice response to chat {chat_id}")
        await self.telegram_service.send_voice_message(chat_id, response_audio)
        logger.info("Voice response sent successfully")


class TextMessageProcessor:
    """Handles text message sending."""

    def __init__(self):
        self.telegram_service = TelegramService()

    async def send_text(self, chat_id: int, text: str) -> None:
        """
        Send text message to Telegram chat.

        Args:
            chat_id: Telegram chat ID
            text: Text message to send
        """
        logger.info(f"Sending text response to chat {chat_id}")
        await self.telegram_service.send_text_message(chat_id, text)
        logger.info("Text response sent successfully")
