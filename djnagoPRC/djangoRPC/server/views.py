from django.shortcuts import render, redirect, get_object_or_404
from .models import ScanInfo, DataServer, SegmentScan, ClientBD, IPAddress, SegmentResult
from .forms import DataServerForm, SegmentScanForm
from django.contrib.auth.decorators import login_required
import ipaddress
import math


@login_required(redirect_field_name=None, login_url='/')
def detail_seg(request, pk):
    item = get_object_or_404(SegmentScan, pk=pk)
    # Получите все объекты SegmentScan
    segment_scans = SegmentScan.objects.all()
    result = SegmentResult.objects.all()

    # Создайте словарь, где ключами будут объекты SegmentScan, а значениями будут связанные IP-адреса
    ip_addresses_by_segment = {}

    # Пройдите по каждому объекту SegmentScan
    for segment_scan in segment_scans:
        # Получите связанные с этим объектом IPAddress
        ip_addresses = IPAddress.objects.filter(seg_scan=segment_scan)

        # Сохраните их в словаре
        ip_addresses_by_segment[segment_scan] = ip_addresses
    ip_dict = []
    for segment_scan, ip_addresses in ip_addresses_by_segment.items():
        if segment_scan == item:
            for ip_address in ip_addresses:
                ip_dict.append(ip_address)

    return render(request, 'server/detail_seg.html', {'item': item,
                                                      'all_ip': ip_dict,
                                                      'result': result
                                                      })


@login_required(redirect_field_name=None, login_url='/')
def remove_item(request, pk):
    item = DataServer.objects.get(pk=pk)
    item.delete()
    return redirect('aim')


@login_required(redirect_field_name=None, login_url='/')
def remove_segment(request, pk):
    item = SegmentScan.objects.get(pk=pk)
    item.delete()
    return redirect('segment')


@login_required(redirect_field_name=None, login_url='/')
def data(request):
    # Count_Ports
    open = ScanInfo.objects.filter(state='open').count()
    filtered = ScanInfo.objects.filter(state='filtered').count()
    close = ScanInfo.objects.filter(state='closed').count()
    open_filtered = ScanInfo.objects.filter(state='open|filtered').count()
    # Count_Task
    client_1 = 0
    client_2 = 0
    data_server = DataServer.objects.in_bulk()
    for id in data_server:
        if data_server[id].tag == 'Done' and data_server[id].client.id == 1:
            client_1 += 1
        if data_server[id].tag == 'Done' and data_server[id].client.id == 2:
            client_2 += 1
    #
    query_results = ScanInfo.objects.all()
    data_serv = DataServer.objects.all()
    data_serv = DataServer.objects.all()
    task_done = DataServer.objects.filter(tag='Done').count()
    error = ''
    if request.method == 'POST':
        form = DataServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aim')
        else:
            error = 'Форма не верна'
    form = DataServerForm()
    tasks = {
        'open': open,
        'filtered': filtered,
        'close': close,
        'open_filtered': open_filtered,
        'form': form,
        'data_serv': data_serv,
        'error': error,
        'section': query_results,
        'task_done': task_done,
        'client_1': client_1,
        'client_2': client_2,
    }
    return render(request, 'server/aim.html', tasks)


@login_required(redirect_field_name=None, login_url='/')
def segment(request):
    scan_segment = SegmentScan.objects.all()
    all_done = IPAddress.objects.filter(
        tag='Done').count() == IPAddress.objects.count()
    if all_done:
        SegmentScan.objects.update(state_scan='Done')
    else:
        pass
    error = ''
    if request.method == 'POST':
        form = SegmentScanForm(request.POST)
        if form.is_valid():
            segment_scan_instance = form.save()
            net = segment_scan_instance.ip
            mask = segment_scan_instance.mask
            network = ipaddress.IPv4Network(f'{net}/{mask}', strict=False)
            segments = [
                ipaddr for ipaddr in network.subnets(prefixlen_diff=4)]
            num_parts = 3
            # Вычисляем, сколько элементов нужно поместить в каждую часть
            part_size = math.ceil(len(segments) / num_parts)
            # Создаем список, в котором каждый элемент - это одна из частей
            segment_parts = [segments[i:i + part_size]
                             for i in range(0, len(segments), part_size)]
            client_bd = ClientBD.objects.all()
            # Создаем словарь с метками для клиентов
            client_processed = {
                alone_cl.id: False for alone_cl in client_bd}
            for addr in segment_parts:
                for alone_cl in client_bd:
                    if not client_processed[alone_cl.id]:
                        for main_ip in addr:
                            client_instance = ClientBD.objects.get(
                                ip_client=alone_cl)
                            IPAddress.objects.create(
                                address=f'{main_ip}', client=client_instance, seg_scan=segment_scan_instance)
                        client_processed[alone_cl.id] = True
                        break
        else:
            error = 'Форма не верна'

    form_segment = SegmentScanForm()

    seg = {
        'form_segment': form_segment,
        'error': error,
        'scan_segment': scan_segment,
    }
    return render(request, 'server/segment.html', seg)
