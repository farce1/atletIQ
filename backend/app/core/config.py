from functools import lru_cache
from pathlib import Path

from uuid import UUID

from pydantic import AnyHttpUrl, PostgresDsn, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.config_utils import (
    EnvironmentType,
    set_env_from_settings,
)

CONVO_MAPPING: dict[str, UUID] = {}


class Settings(BaseSettings):
    PROJECT_NAME: str = "atlet-iq"
    SERVER_HOST: AnyHttpUrl
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.0.1"

    DEBUG: bool = False
    ENABLE_ADVANCED_MODELS: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.TEST

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    BACKEND_CORS_ALLOW_ALL: bool = False

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Sentry
    SENTRY_ENABLED: bool = False
    SENTRY_DSN: str | None = None
    SENTRY_SAMPLES_RATE: float = 0.5
    SENTRY_ENV: str | None = None

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "library"
    DB_USER: str = "user"
    DB_PASSWORD: SecretStr = SecretStr("password")

    @property
    def DATABASE_URI(self) -> PostgresDsn:  # noqa: N802
        return PostgresDsn(
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )

    LOGGING_CONF_FILE: str = "logging.conf"

    # Integrations
    # ------------>

    # Claude Agent Configuration
    CLAUDE_AGENT_SYSTEM_PROMPT: str = (
        "You are a specialized, intelligent AI assistant designated to help users with their queries."
    )
    CLAUDE_AGENT_ALLOWED_TOOLS: list[str] = ["Read", "Write", "Bash", "WebSearch"]
    CLAUDE_AGENT_PERMISSION_MODE: str = "acceptEdits"
    CLAUDE_AGENT_WORKING_DIR: str | None = None
    CLAUDE_AGENT_MAX_CONVERSATION_LENGTH: int = 50
    CLAUDE_AGENT_ENABLE_STREAMING: bool = False

    @field_validator("BACKEND_CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v

        # This should never be reached given the type annotation, but ensures type safety
        raise ValueError(f"Unexpected type for BACKEND_CORS_ORIGINS: {type(v)}")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=str(Path(__file__).parent.parent.parent / "config" / ".env"),
        extra="allow",
    )


@lru_cache()
@set_env_from_settings
def get_settings() -> Settings:
    return Settings()  # type: ignore[missing-argument]


settings = get_settings()
