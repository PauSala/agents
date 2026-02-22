from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from core.events import UINotifier


class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    trace_id: str
    agent: str
    event: str
    data: dict[str, Any] = Field(default_factory=dict)


class LogCollector:
    """Shared structured log collector for tracing agent decisions."""

    def __init__(self, trace_id: str | None = None, emitter: UINotifier | None = None):
        self.trace_id = trace_id or uuid4().hex[:12]
        self.entries: list[LogEntry] = []

    def log(self, agent: str, event: str, **data: Any) -> None:
        self.entries.append(LogEntry(trace_id=self.trace_id, agent=agent, event=event, data=data))

    def summary(self) -> str:
        lines: list[str] = [f"trace: {self.trace_id}"]
        for entry in self.entries:
            ts = entry.timestamp.strftime("%H:%M:%S.%f")[:-3]
            data_str = ", ".join(f"{k}={v}" for k, v in entry.data.items())
            lines.append(f"[{ts}] {entry.agent} :: {entry.event}" + (f" | {data_str}" if data_str else ""))
        return "\n".join(lines)
