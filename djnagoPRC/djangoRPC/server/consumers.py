# В вашем consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer


class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add(
            'real_time_graphs',
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Отсоедините клиента от группы WebSocket при разрыве соединения
        await self.channel_layer.group_discard(
            'real_time_graphs',
            self.channel_name
        )

    async def graph_data_update(self, event):
        await self.send(event['data'])


class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add(
            'send_client_data',
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'send_client_data',
            self.channel_name
        )

    async def client_data_update(self, event):
        await self.send(event['client_1'])
