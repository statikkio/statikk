# realtime_server.py
from __future__ import annotations

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins; adjust for security
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class ConnectionManager:
    """
    Manages WebSocket connections and subscriptions for real-time updates.

    Attributes:
        active_connections (List[WebSocket]): A list of active WebSocket connections.
        subscriptions (Dict[str, List[WebSocket]]): A mapping of collection names to subscribed WebSocket connections.
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.subscriptions: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        """
        Accepts a new WebSocket connection and adds it to the active connections list.

        :param websocket: The WebSocket connection to add.
        :type websocket: WebSocket
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list and subscriptions.

        :param websocket: The WebSocket connection to remove.
        :type websocket: WebSocket
        """
        self.active_connections.remove(websocket)
        for subscribers in self.subscriptions.values():
            if websocket in subscribers:
                subscribers.remove(websocket)

    async def subscribe(self, websocket: WebSocket, collection: str):
        """
        Subscribes a WebSocket connection to a specific collection.

        :param websocket: The WebSocket connection to subscribe.
        :type websocket: WebSocket
        :param collection: The collection to subscribe to.
        :type collection: str
        """
        if collection not in self.subscriptions:
            self.subscriptions[collection] = []
        self.subscriptions[collection].append(websocket)

    async def send_update(self, collection: str, message: dict):
        """
        Sends a real-time update to all WebSocket connections subscribed to a collection.

        :param collection: The collection whose subscribers will receive the update.
        :type collection: str
        :param message: The message containing the update.
        :type message: dict
        """
        if collection in self.subscriptions:
            subscribers = self.subscriptions[collection]
            for connection in subscribers:
                await connection.send_json(message)


manager = ConnectionManager()


@app.websocket('/ws/{project_id}/{collection}')
async def websocket_endpoint(websocket: WebSocket, project_id: str, collection: str):
    """
    WebSocket endpoint for real-time data sync. Manages connections and subscriptions.

    :param websocket: The WebSocket connection instance.
    :type websocket: WebSocket
    :param project_id: The project ID associated with the WebSocket connection.
    :type project_id: str
    :param collection: The collection the client wants to subscribe to.
    :type collection: str
    """
    await manager.connect(websocket)
    await manager.subscribe(websocket, collection)
    try:
        while True:
            # Keep the connection open; receive any incoming messages if needed
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
