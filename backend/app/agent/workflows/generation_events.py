from llama_index.core.workflow import Event

from app.schemas.agent.task_types import TaskType


class ErrorEvent(Event):
    error_step: str
    error: Exception
    error_msg: str | None


class TextEvaluationEvent(Event):
    message: str


class TextGenerationEvent(Event):
    message: str
    task_type: TaskType


class GuardrailsEvent(Event):
    message: str
    task_type: TaskType


class TextRefusalEvent(Event):
    message: str
    refusal_reason: str
