from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import logging


from .models import ScanInfo, DataServer, ResultPortsAim, LevelCve, IPAddress, SegmentResult

from django.db.models import Count

channel_layer = get_channel_layer()

@receiver(post_save, sender=SegmentResult)
def update_table_res(sender, instance, created, **kwargs):
    
    if created:
        pass

    if instance.is_execution_complete:
        
        host = instance.host
        state_scan = instance.state_scan
        mode = instance.result.seg_scan.mode
        state_ports = instance.state_ports

        row_count = SegmentResult.objects.count()

        if mode == 'OS':
            full_name = instance.full_name
            vendor = instance.vendor
            osfamily = instance.osfamily
            osgen = instance.osgen
            accuracy = instance.accuracy
        else:
            full_name = ''
            vendor = ''
            osfamily = ''
            osgen = ''
            accuracy = ''

        data = {

            'row_count': row_count,
            'id': instance.pk,
            'host': host,
            'state_scan': state_scan,
            'mode': mode,
            'state_ports': state_ports,
            'full_name': full_name,
            'vendor': vendor,
            'osfamily': osfamily,
            'osgen': osgen,
            'accuracy': accuracy
        }


        async def send_data_table_seg():
            await channel_layer.group_send(
                'send_data_table_seg',
                {
                    'type': 'data_table_seg.update',
                    'data': data
                }
            )


        async_to_sync(send_data_table_seg)()

@receiver(post_save, sender=IPAddress)
def update_seg_client_data(sender, instance, created, **kwargs):
    
    if created:
        pass
    else:
        new_tag = instance.tag
        new_cl = instance.client.ip_client

        # Отправьте это значение через WebSocket

        async def send_seg_table_update():
            await channel_layer.group_send('my_seg_table_group', {
                'type': 'seg_update_tag',
                'tag': new_tag,
                'client': new_cl,
                'id': instance.pk,  # Идентификатор записи, которую вы обновили
            })

        async_to_sync(send_seg_table_update)()
        
    client_1 = 0
    client_2 = 0
    client_3 = 0
    data_server = IPAddress.objects.filter(seg_scan=instance.seg_scan).in_bulk()
    for id in data_server:
        
        if data_server[id].tag == 'Done' and data_server[id].client.id == 1:
            client_1 += 1
        if data_server[id].tag == 'Done' and data_server[id].client.id == 2:
            client_2 += 1
        if data_server[id].tag == 'Done' and data_server[id].client.id == 3:
            client_3 += 1
    client_data = {

        'client_1': client_1,
        'client_2': client_2,
        'client_3': client_3,

    }

    task_done = IPAddress.objects.filter(seg_scan=instance.seg_scan, tag='Done').count()
    
    async def send_seg_client_data():
        await channel_layer.group_send(
            'send_client_data_seg',
            {
                'type': 'client_data.update',
                'client': client_data
            }
        )

    async def send_seg_task_done():
        await channel_layer.group_send(
            'send_task_seg_done',
            {
                'type': 'task_done.update',
                'task': task_done
            }
        )

    async_to_sync(send_seg_client_data)()

    async_to_sync(send_seg_task_done)()

@receiver(post_save, sender=LevelCve)
def update_cve_year_data(sender, instance, **kwargs):
    # Создаем словарь для хранения количества уникальных уровней уязвимостей для каждого года
    # Создаем словарь для хранения количества уровней уязвимостей для каждого года
    vulnerability_counts_by_year = {}

    # Получаем уникальные года
    unique_years = LevelCve.objects.filter(result__result__seg_scan=instance.result.result.seg_scan).values('year').distinct()

    # Итерируемся по уникальным годам и подсчитываем уровни уязвимостей
    for year_info in unique_years:
        year = year_info['year']


        critical_count = LevelCve.objects.filter(year=year, level='Критичная').count()


        high_count = LevelCve.objects.filter(year=year, level='Высокая').count()


        medium_count = LevelCve.objects.filter(year=year, level='Средняя').count()
        
        
        normal_count = LevelCve.objects.filter(year=year, level='Низкая').count()

        # Создаем словарь для уровней уязвимостей текущего года
        levels_dict = {
            'Критичная': critical_count,
            'Высокая': high_count,
            'Средняя': medium_count,
            'Низкая': normal_count
        }

        # Добавляем в общий словарь
        vulnerability_counts_by_year[year] = levels_dict

    async def send_cve_year_data():
        await channel_layer.group_send(
            'send_data_information_cve_data',
            {
                'type': 'cve_data.update',
                'data': vulnerability_counts_by_year
            }
        )


    async_to_sync(send_cve_year_data)()


@receiver(post_save, sender=ScanInfo)
def update_table_data(sender, instance, **kwargs):

    host = instance.host
    state_scan = instance.state_scan
    mode = instance.result.mode
    state_ports = instance.state_ports
    
    row_count = ScanInfo.objects.count()
    
    if mode == 'OS':
        full_name = instance.full_name
        vendor = instance.vendor
        osfamily = instance.osfamily
        osgen = instance.osgen
        accuracy = instance.accuracy
    else:
        full_name = ''
        vendor = ''
        osfamily = ''
        osgen = ''
        accuracy = ''
    
    data = {
        
        'row_count': row_count,
        'id': instance.pk,
        'host': host,
        'state_scan': state_scan,
        'mode': mode,
        'state_ports': state_ports,
        'full_name': full_name,
        'vendor': vendor,
        'osfamily': osfamily,
        'osgen': osgen,
        'accuracy': accuracy
    }
    
    
    async def send_data_table():
        await channel_layer.group_send(
            'send_data_table',
            {
                'type': 'data_table.update',
                'data': data
            }
        )


    async_to_sync(send_data_table)()


@receiver(post_save, sender=DataServer)
def update_client_data(sender, instance, **kwargs):

    client_1 = 0
    client_2 = 0
    client_3 = 0
    data_server = DataServer.objects.in_bulk()
    for id in data_server:
        if data_server[id].tag == 'Done' and data_server[id].client.id == 4:
            client_1 += 1
        if data_server[id].tag == 'Done' and data_server[id].client.id == 5:
            client_2 += 1
        if data_server[id].tag == 'Done' and data_server[id].client.id == 6:
            client_3 += 1    
    client_data = {

        'client_1': client_1,
        'client_2': client_2,
        'client_3': client_3


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
