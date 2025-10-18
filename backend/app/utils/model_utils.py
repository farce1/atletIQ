from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.constants import DEFAULT_TEMPERATURE
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from app.core.config import settings


def get_llm_openai(
    model: str = settings.LLM_MODEL_DEFAULT,
    timeout: int = settings.LLM_TIMEOUT_DEFAULT,
    temperature: float = DEFAULT_TEMPERATURE,
) -> FunctionCallingLLM:
    return OpenAI(
        model=model,
        request_timeout=timeout,
        api_key=settings.OPENAI_API_KEY,
        temperature=temperature,
    )


def get_embedding_model() -> BaseEmbedding:
    return OpenAIEmbedding(
        model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY
    )
