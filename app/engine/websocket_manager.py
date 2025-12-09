from typing import List
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    async def broadcast(self, message: str):
        for ws in self.active_connections:
            await ws.send_text(message)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

manager = WebSocketManager()
