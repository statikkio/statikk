from __future__ import annotations

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Manages active connections and subscriptions


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.subscriptions: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        for subscribers in self.subscriptions.values():
            if websocket in subscribers:
                subscribers.remove(websocket)

    async def subscribe(self, websocket: WebSocket, collection: str):
        if collection not in self.subscriptions:
            self.subscriptions[collection] = []
        self.subscriptions[collection].append(websocket)

    async def send_update(self, collection: str, message: dict):
        if collection in self.subscriptions:
            subscribers = self.subscriptions[collection]
            for connection in subscribers:
                await connection.send_json(message)


manager = ConnectionManager()


@app.websocket('/ws/{project_id}/{collection}')
async def websocket_endpoint(websocket: WebSocket, project_id: str, collection: str):
    await manager.connect(websocket)
    await manager.subscribe(websocket, collection)
    try:
        while True:
            await websocket.receive_text()
            # This is where the server can handle incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)
