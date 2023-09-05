# В вашем consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import ScanInfo, DataServer


class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add(
            'real_time_graphs',
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

        if message['type'] == 'get_initial_data':
            # Здесь вы можете выполнить логику для получения начальных данных

            open = await sync_to_async(ScanInfo.objects.filter(state='open').count)()
            filtered = await sync_to_async(ScanInfo.objects.filter(state='filtered').count)()
            close = await sync_to_async(ScanInfo.objects.filter(state='closed').count)()
            open_filtered = await sync_to_async(ScanInfo.objects.filter(state='open|filtered').count)()
            print(open)

            initial_data = {
                'open': open,
                'filtered': filtered,
                'close': close,
                'open_filtered': open_filtered,
            }

            # Отправляем начальные данные обратно клиенту
            await self.send(json.dumps({
                'type': 'initial_data',
                'data': initial_data,
            }))

    async def disconnect(self, close_code):
        # Отсоедините клиента от группы WebSocket при разрыве соединения
        await self.channel_layer.group_discard(
            'real_time_graphs',
            self.channel_name
        )

    async def graph_data_update(self, event):
        await self.send(json.dumps({'data': event['data']}))


class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add(
            'send_client_data',
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

        if message['type'] == 'get_cl_data':
            # Здесь вы можете выполнить логику для получения начальных данных

            @sync_to_async
            def get_cl_data():
                client_1 = 0
                client_2 = 0
                data_server = DataServer.objects.in_bulk()
                for id in data_server:
                    if data_server[id].tag == 'Done' and data_server[id].client.id == 1:
                        client_1 += 1
                    if data_server[id].tag == 'Done' and data_server[id].client.id == 2:
                        client_2 += 1
                return {
                    'client_1': client_1,
                    'client_2': client_2
                }

            # Внутри вашего обработчика или функции, где требуется получить client_data:

            client_data = await get_cl_data()

            print(client_data)

            # Отправляем начальные данные обратно клиенту
            await self.send(json.dumps({
                'type': 'initial_data',
                'data': client_data,
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'send_client_data',
            self.channel_name
        )

    async def client_data_update(self, event):
        await self.send(json.dumps({'data': event['client']}))


class TableConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def send_data_to_clients(self):
        data_serv = DataServer.objects.all()
        data_to_send = []
        for item in data_serv:
            data_to_send.append({
                'id': item.id,
                'ip': item.ip,
                'port': item.port,
                'mode': item.mode,
                'client_scan': item.client,
                'tag': item.tag,  # Включите информацию о теге
            })
        await self.channel_layer.group_send(
            'table_update_group',
            {
                'type': 'table.update',
                'data': json.dumps(data_to_send),
            }
        )

    async def disconnect(self, close_code):
        await self.close()
