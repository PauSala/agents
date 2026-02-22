
from core.types import AgentEvent
from server.server import ConnectionManager


class UINotifier:
    def __init__(self, websocket_manager: ConnectionManager):
        self.manager = websocket_manager

    async def notify(self, event: AgentEvent):
        await self.manager.broadcast(event)