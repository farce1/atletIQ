from io import BytesIO
from typing import BinaryIO

from elevenlabs import ElevenLabs

from app.core.config import settings


class TextToSpeechService:
    def __init__(self) -> None:
        if not settings.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY is not configured in settings")
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY.get_secret_value())

    async def convert_text_to_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str,
        output_format: str,
    ) -> BinaryIO:
        """
        Converts text to speech using ElevenLabs API.

        Args:
            text: The text to convert to speech
            voice_id: The ElevenLabs voice ID
            model_id: The model ID for synthesis
            output_format: The audio output format

        Returns:
            BinaryIO: Audio data as a binary stream
        """
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

        return audio_buffer
