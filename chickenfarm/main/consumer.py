import asyncio, json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class ClientConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_recieve(self, event):
        print("recieve", event)

    async def websocket_disconnect(self, event):
        print("dis connected", event)
        await self.send({
            "type": "websocket.disconnect"
        })

class DeviceConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_recieve(self, event):
        print("recieve", event)

    async def websocket_disconnect(self, event):
        print("dis connected", event)
        await self.send({
            "type": "websocket.disconnect"
        })