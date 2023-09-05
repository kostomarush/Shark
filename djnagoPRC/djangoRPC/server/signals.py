from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging


from .models import ScanInfo, DataServer

channel_layer = get_channel_layer()


@receiver(post_save, sender=DataServer)
def update_client_data(sender, instance, **kwargs):

    client_1 = 0
    client_2 = 0
    data_server = DataServer.objects.in_bulk()
    for id in data_server:
        if data_server[id].tag == 'Done' and data_server[id].client.id == 1:
            client_1 += 1
        if data_server[id].tag == 'Done' and data_server[id].client.id == 2:
            client_2 += 1
    print(client_1)
    client_data = {

        'client_1': client_1,
        'client_2': client_2

    }

    async def send_client_data():
        await channel_layer.group_send(
            'send_client_data',
            {
                'type': 'client_data.update',
                'client': client_data
            }
        )

    async_to_sync(send_client_data)()


@receiver(post_save,  sender=ScanInfo)
def update_graph_data(sender, instance, **kwargs):

    def get_scan_info_count(state):
        count = ScanInfo.objects.filter(state=state).count()
        return count

    open = get_scan_info_count('open')
    filtered = get_scan_info_count('filtered')
    close = get_scan_info_count('closed')
    open_filtered = get_scan_info_count('open|filtered')
    graph_data = {
        'open': open,
        'filtered': filtered,
        'close': close,
        'open_filtered': open_filtered
    }

    async def send_graph_data():
        await channel_layer.group_send(
            'real_time_graphs',
            {
                'type': 'graph_data.update',
                'data': graph_data
            }
        )

    async_to_sync(send_graph_data)()

