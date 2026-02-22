from __future__ import annotations

import asyncio

from core.types import AgentEvent
from server.types import ConnectionManager


class NoOpEmitter:
    def notify(self, event: AgentEvent) -> None:
        print(event.model_dump_json())
        pass


class WebSocketEmitter:
    def __init__(self, websocket_manager: ConnectionManager):
        self.manager = websocket_manager

    def notify(self, event: AgentEvent) -> None:
        async def _safe():
            await self.manager.broadcast(event)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(_safe())
        else:
            loop.create_task(_safe())
