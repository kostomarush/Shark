from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging


from .models import ScanInfo, DataServer, ResultPortsAim

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
    client_data = {

        'client_1': client_1,
        'client_2': client_2

    }

    task_done = DataServer.objects.filter(tag='Done').count()

    async def send_client_data():
        await channel_layer.group_send(
            'send_client_data',
            {
                'type': 'client_data.update',
                'client': client_data
            }
        )

    async def send_task_done():
        await channel_layer.group_send(
            'send_task_done',
            {
                'type': 'task_done.update',
                'task': task_done
            }
        )

    async_to_sync(send_client_data)()

    async_to_sync(send_task_done)()
    
@receiver(post_save, sender=DataServer)
def update_client_tag(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        new_tag = instance.tag
        new_cl = instance.client.ip_client

        # Отправьте это значение через WebSocket

        async def send_update():
            await channel_layer.group_send('my_table_group', {
                'type': 'update_tag',
                'tag': new_tag,
                'client': new_cl,
                'id': instance.pk,  # Идентификатор записи, которую вы обновили
            })

        async_to_sync(send_update)()

@receiver(post_save,  sender=ResultPortsAim)
def update_graph_data(sender, instance, **kwargs):

    def get_scan_info_count(state):
        count = ResultPortsAim.objects.filter(state=state).count()
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
