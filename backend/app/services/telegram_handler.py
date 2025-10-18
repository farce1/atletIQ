import logging
from sqlalchemy.orm import Session

from app.schemas.telegram_schemas import TelegramMessage
from app.services.telegram_message_processor import (
    TelegramMessageProcessor,
    VoiceMessageProcessor,
    TextMessageProcessor,
)

logger = logging.getLogger(__name__)


class TelegramMessageHandler:
    """Routes Telegram messages to appropriate handlers."""

    def __init__(self, db: Session):
        self.message_processor = TelegramMessageProcessor(db=db)
        self.voice_processor = VoiceMessageProcessor()
        self.text_processor = TextMessageProcessor()

    async def handle_message(self, message: TelegramMessage) -> None:
        """
        Route message to appropriate handler based on message type.

        Args:
            message: TelegramMessage to process
        """
        chat_id = message.chat.id

        if message.voice:
            logger.info(f"Routing voice message from chat {chat_id}")

            # Download and transcribe
            transcribed_text = await self.voice_processor.download_and_transcribe(
                message.voice.file_id
            )

            # Get AI response
            response_text = await self.message_processor.process_query(
                transcribed_text, chat_id
            )

            # Send voice response
            await self.voice_processor.convert_and_send_voice(chat_id, response_text)

        elif message.text:
            logger.info(f"Routing text message from chat {chat_id}")

            # Get AI response
            response_text = await self.message_processor.process_query(
                message.text, chat_id
            )

            # Send text response
            await self.text_processor.send_text(chat_id, response_text)

        else:
            logger.warning(f"Unsupported message type from chat {chat_id}")
            raise ValueError("Unsupported message type (neither text nor voice)")
