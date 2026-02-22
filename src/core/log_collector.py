from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from core.events import EventEmitter
from core.types import AgentEvent


class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    trace_id: str
    agent: str
    event: str
    data: dict[str, Any] = Field(default_factory=dict)


class LogCollector:
    """Shared structured log collector for tracing agent decisions."""

    def __init__(self, emitter: EventEmitter, trace_id: str | None = None):
        self.trace_id = trace_id or uuid4().hex[:12]
        self.entries: list[LogEntry] = []
        self.emitter = emitter

    def log(self, agent: str, event: str, **data: Any) -> None:
        entry = LogEntry(trace_id=self.trace_id, agent=agent, event=event, data=data)
        self.entries.append(entry)
        self.emitter.notify(
            AgentEvent(
                agent=entry.agent,
                status=entry.event,
                data=entry.data,
                timestamp=entry.timestamp,
            )
        )

    def summary(self) -> str:
        lines: list[str] = [f"trace: {self.trace_id}"]
        for entry in self.entries:
            ts = entry.timestamp.strftime("%H:%M:%S.%f")[:-3]
            data_str = ", ".join(f"{k}={v}" for k, v in entry.data.items())
            lines.append(
                f"[{ts}] {entry.agent} :: {entry.event}"
                + (f" | {data_str}" if data_str else "")
            )
        return "\n".join(lines)
