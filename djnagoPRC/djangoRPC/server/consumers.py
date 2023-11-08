# В вашем consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import ScanInfo, DataServer, ResultPortsAim


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

            open = await sync_to_async(ResultPortsAim.objects.filter(state='open').count)()
            filtered = await sync_to_async(ResultPortsAim.objects.filter(state='filtered').count)()
            close = await sync_to_async(ResultPortsAim.objects.filter(state='closed').count)()
            open_filtered = await sync_to_async(ResultPortsAim.objects.filter(state='open|filtered').count)()
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
        # Присоедините клиента к группе WebSocket
        await self.channel_layer.group_add('my_table_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Отсоедините клиента от группы WebSocket при разрыве соединения
        await self.channel_layer.group_discard('my_table_group', self.channel_name)

    async def update_tag(self, event):
        # Этот метод вызывается, когда сигнал об обновлении "tag" отправляется
        tag = event['tag']
        client = event['client']
        record_id = event['id']
        # Отправьте обновленные данные клиенту
        await self.send(json.dumps({
            'id': record_id,
            'tag': tag,
            'client': client
        }))

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Присоедините клиента к группе WebSocket
        await self.channel_layer.group_add('send_task_done', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Отсоедините клиента от группы WebSocket при разрыве соединения
        await self.channel_layer.group_discard('send_task_done', self.channel_name)

    async def task_done_update(self, event):
        # Этот метод вызывается, когда сигнал об обновлении "tag" отправляется
        task = event['task']

        # Отправьте обновленные данные клиенту
        await self.send(json.dumps({
            'task': task,
        }))


