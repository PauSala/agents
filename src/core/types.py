from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from typing import Protocol

T = TypeVar("T")


class AgentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"
    RETRY = "retry"
    EXHAUSTED = "exhausted"
    END = "end"


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
    agent_id: str
    caller_id: str
    status: str
    data: dict[str, Any]
    timestamp: datetime


class EventEmitter(Protocol):
    def notify(self, event: AgentEvent) -> None: ...
