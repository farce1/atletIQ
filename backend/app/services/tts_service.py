from io import BytesIO
from typing import BinaryIO
import logging

from elevenlabs import ElevenLabs

from app.core.config import settings

logger = logging.getLogger(__name__)


class TextToSpeechService:
    def __init__(self) -> None:
        if not settings.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY is not configured in settings")
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY.get_secret_value())

    async def convert_speech_to_text(self, audio_file: BinaryIO) -> str:
        """
        Converts speech to text using ElevenLabs API.

        Args:
            audio_file: The audio file as a binary stream

        Returns:
            str: Transcribed text
        """
        try:
            logger.info("Starting speech-to-text conversion")

            # Reset buffer to beginning
            audio_file.seek(0)

            # Get file size for logging
            audio_file.seek(0, 2)  # Seek to end
            file_size = audio_file.tell()
            audio_file.seek(0)  # Reset to beginning
            logger.info(f"Audio file size: {file_size} bytes")

            # Use ElevenLabs speech-to-text
            # The convert method expects 'file' parameter, not 'audio'
            result = self.client.speech_to_text.convert(
                file=audio_file,
                model_id="scribe_v1",
                enable_logging=True,
            )

            # Extract text from result
            transcribed_text = result.text if hasattr(result, 'text') else str(result)
            logger.info(f"Transcription result: {transcribed_text}")

            return transcribed_text
        except Exception as e:
            logger.error(f"Error in speech-to-text conversion: {str(e)}")
            raise

    async def convert_text_to_speech(
        self,
        text: str,
        voice_id: str | None = None,
        model_id: str | None = None,
        output_format: str | None = None,
    ) -> BinaryIO:
        """
        Converts text to speech using ElevenLabs API.

        Args:
            text: The text to convert to speech
            voice_id: The ElevenLabs voice ID (defaults to settings value)
            model_id: The model ID for synthesis (defaults to settings value)
            output_format: The audio output format (defaults to settings value)

        Returns:
            BinaryIO: Audio data as a binary stream
        """
        # Use settings defaults if not provided
        voice_id = voice_id or settings.ELEVENLABS_VOICE_ID
        model_id = model_id or settings.ELEVENLABS_MODEL_ID
        output_format = output_format or settings.ELEVENLABS_OUTPUT_FORMAT

        logger.info(f"Converting text to speech: {text[:50]}...")

        audio_generator = self.client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
            output_format=output_format,
        )

        # Collect audio chunks into a BytesIO buffer
        audio_buffer = BytesIO()
        for chunk in audio_generator:
            audio_buffer.write(chunk)

        # Reset buffer position to beginning
        audio_buffer.seek(0)

        logger.info("Text-to-speech conversion completed")

        return audio_buffer
