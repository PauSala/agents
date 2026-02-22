from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from core.events import WebSocketEmitter
from orchestration.main_flow import Director
from fastapi import BackgroundTasks

from server.types import ConnectionManager

app = FastAPI()



manager = ConnectionManager()
director = Director(emitter=WebSocketEmitter(websocket_manager=manager))


# --- Data Models ---
class UserPrompt(BaseModel):
    prompt: str


# --- Endpoints ---


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    The frontend connects here to receive real-time agent updates.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/run")
async def run_pipeline(data: UserPrompt, background_tasks: BackgroundTasks):
    # This sends the response to the UI immediately 
    # while the Director works in the background
    background_tasks.add_task(director.run, data.prompt)
    return {"status": "request_received"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
