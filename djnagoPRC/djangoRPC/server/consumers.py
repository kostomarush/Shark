import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ScanInfo

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        data = await sync_to_async(self.get_graph_data)()  # Получение данных для графика из базы данных
        await self.send(json.dumps(data))
        

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass


    async def get_date(self):
        data = await sync_to_async(self.get_graph_data)()  # Получение данных для графика из базы данных
        await self.send(json.dumps(data))

    @staticmethod
    def get_graph_data():
        open = GraphConsumer.get_scan_info_count('open')
        filtered = GraphConsumer.get_scan_info_count('filtered')
        close = GraphConsumer.get_scan_info_count('closed')
        open_filtered = GraphConsumer.get_scan_info_count('open|filtered')
        return [open, filtered, close, open_filtered]

    @staticmethod
    def get_scan_info_count(state):
        count = ScanInfo.objects.filter(state=state).count()
        return count