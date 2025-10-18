# flake8: noqa
from pydantic import BaseModel


class ToolPrompt(BaseModel):
    name: str
    description: str


SAMPLE_TOOL_PROMPT = ToolPrompt(
    name="sample_tool",
    description=(
        "Tool designed to retrieve and aswer questions related to sample data."
    ),
)
