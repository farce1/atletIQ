from enum import Enum
from typing import Any, Callable, Generator

from functools import wraps

CallableGenerator = Generator[Callable[..., Any], None, None]


class EnvironmentType(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


def set_env_from_settings(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to set environment variables from settings.
    This decorator is useful for encrypted fields and providers that
    require API keys to be available as environment variables.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        settings = func(*args, **kwargs)
        # os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        return settings  # noqa: RET504

    return wrapper
