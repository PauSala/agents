from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    agent: str
    event: str
    data: dict[str, Any] = Field(default_factory=dict)


class LogCollector:
    """Shared structured log collector for tracing agent decisions."""

    def __init__(self):
        self.entries: list[LogEntry] = []

    def log(self, agent: str, event: str, **data: Any) -> None:
        self.entries.append(LogEntry(agent=agent, event=event, data=data))

    def summary(self) -> str:
        lines: list[str] = []
        for entry in self.entries:
            ts = entry.timestamp.strftime("%H:%M:%S.%f")[:-3]
            data_str = ", ".join(f"{k}={v}" for k, v in entry.data.items())
            lines.append(f"[{ts}] {entry.agent} :: {entry.event}" + (f" | {data_str}" if data_str else ""))
        return "\n".join(lines)
