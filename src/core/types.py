from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


@dataclass(frozen=True)
class ErrorInfo:
    message: str
    stage: str  # "inference", "validation", "tool_execution", "routing"


@dataclass(frozen=True)
class Result(Generic[T]):
    ok: bool
    value: T | None = None
    error: ErrorInfo | None = None


def Ok(value: T) -> Result[T]:
    """Create a success Result. Type of T is inferred from the argument."""
    return Result(ok=True, value=value)


def Err(message: str, stage: str) -> Result[Any]:
    """Create a failure Result."""
    return Result(ok=False, error=ErrorInfo(message=message, stage=stage))


class AgentEvent(BaseModel):
    agent: str
    status: str
    data: dict[str, Any]
    timestamp: datetime
