from pydantic import BaseModel, Field


class TextToSpeechRequest(BaseModel):
    text: str = Field(..., description="The text to convert to speech", min_length=1)
    voice_id: str = Field(
        default="kdmDKE6EkgrWrrykO9Qt",
        description="The ElevenLabs voice ID to use for text-to-speech",
    )
    model_id: str = Field(
        default="eleven_multilingual_v2",
        description="The model ID to use for synthesis",
    )
    output_format: str = Field(
        default="mp3_44100_128",
        description="The desired audio output format",
    )
