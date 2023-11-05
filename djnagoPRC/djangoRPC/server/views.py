from django.shortcuts import render, redirect, get_object_or_404
from .models import ScanInfo, DataServer, SegmentScan, ClientBD, IPAddress, SegmentResult, ResultPorts, CveInformation, ResultPortsAim, CveInformationAim
from .forms import DataServerForm, SegmentScanForm
from django.contrib.auth.decorators import login_required
import ipaddress
import math


@login_required(redirect_field_name=None, login_url='/')
def detail_seg(request, pk):
    item = get_object_or_404(SegmentScan, pk=pk)
    segment_scans = SegmentScan.objects.all()
    all_ip_addresses = IPAddress.objects.all()

    # Создайте словарь, где ключами будут объекты SegmentScan, а значениями будут связанные IP-адреса
    ip_addresses_by_segment = {}
    segment_results_by_segment = {}

    for all_ip_address in all_ip_addresses:

        segment_results = SegmentResult.objects.filter(result=all_ip_address)

        segment_results_by_segment[all_ip_address] = segment_results

    result_dict = []
    for all_ip_address, segment_results in segment_results_by_segment.items():
        if all_ip_address.seg_scan == item:
            for result in segment_results:
                result_dict.append(result)

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
                                                      'result': result_dict
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
    query_results = ScanInfo.objects.all()
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
        'form': form,
        'data_serv': data_serv,
        'error': error,
        'section': query_results,
        'task_done': task_done,
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
                ipaddr for ipaddr in network.subnets(prefixlen_diff=6)]
            for addr in segments:
                IPAddress.objects.create(
                    address=f'{addr}', seg_scan=segment_scan_instance)
        else:
            error = 'Форма не верна'

    form_segment = SegmentScanForm()

    seg = {
        'form_segment': form_segment,
        'error': error,
        'scan_segment': scan_segment,
    }
    return render(request, 'server/segment.html', seg)


def port_information(request, pk):
    item = get_object_or_404(SegmentResult, pk=pk)
    segment_results = SegmentResult.objects.all()
    ports_by_host = {}
    # Пройдите по каждому объекту SegmentScan
    for segment_result in segment_results:
        # Получите связанные с этим объектом IPAddress
        ports = ResultPorts.objects.filter(all_info=segment_result)

        # Сохраните их в словаре
        ports_by_host[segment_result] = ports

    port_dict = []
    for ports, segment_result in ports_by_host.items():
        if ports == item:
            for ports in segment_result:
                port_dict.append(ports)

    return render(request, 'server/port_information.html', {'item': item,
                                                            'port_dict': port_dict})



def cve_information(request, pk):
    item = get_object_or_404(ResultPorts, pk=pk)
    port_results = ResultPorts.objects.all()
    cve_by_port = {}
    # Пройдите по каждому объекту SegmentScan
    for port_result in port_results:
        # Получите связанные с этим объектом IPAddress
        cve = CveInformation.objects.filter(result_ports=port_result)

        # Сохраните их в словаре
        cve_by_port[port_result] = cve

    cve_dict = []
    for cve, port_result in cve_by_port.items():
        if cve == item:
            for i in port_result:
                cve_dict.append(i)

    return render(request, 'server/cve_information.html', {'item': item,
                                                            'cve_dict': cve_dict})



def port_info_aim(request, pk):
    item = get_object_or_404(ScanInfo, pk=pk)
    scan_results = ScanInfo.objects.all()
    ports_by_host = {}
    # Пройдите по каждому объекту SegmentScan
    for scan_result in scan_results:
        # Получите связанные с этим объектом IPAddress
        ports = ResultPortsAim.objects.filter(all_info=scan_result)

        # Сохраните их в словаре
        ports_by_host[scan_result] = ports

    port_dict = []
    for ports, scan_result in ports_by_host.items():
        if ports == item:
            for ports in scan_result:
                port_dict.append(ports)

    return render(request, 'server/port_info_aim.html', {'item': item,
                                                         'port_dict': port_dict})


def cve_information_aim(request, pk):
    item = get_object_or_404(ResultPortsAim, pk=pk)
    port_results = ResultPortsAim.objects.all()
    cve_by_port = {}
    # Пройдите по каждому объекту SegmentScan
    for port_result in port_results:
        # Получите связанные с этим объектом IPAddress
        cve = CveInformationAim.objects.filter(result_ports=port_result)

        # Сохраните их в словаре
        cve_by_port[port_result] = cve

    cve_dict = []
    for cve, port_result in cve_by_port.items():
        if cve == item:
            for i in port_result:
                cve_dict.append(i)

    return render(request, 'server/cve_information_aim.html', {'item': item,
                                                            'cve_dict': cve_dict})