
# --- Connection Manager ---
from fastapi import WebSocket

from core.types import AgentEvent


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: AgentEvent):
        print(message)
        for connection in self.active_connections:
            await connection.send_json(message.model_dump_json())