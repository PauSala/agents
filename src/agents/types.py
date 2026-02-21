from typing import Any

from pydantic import BaseModel


class ToolSelection(BaseModel):
    """Schema for tool execution."""
    tool_name: str
    prompt: str

class ToolCall(BaseModel):
    """Schema for tool execution."""
    arguments: dict[str, Any]
