from django.shortcuts import render, redirect, get_object_or_404
from .models import ScanInfo, DataServer, SegmentScan
from .forms import DataServerForm, SegmentScanForm
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None, login_url='/')
def detail_seg(request, pk):
    item = get_object_or_404(SegmentScan, pk=pk)
    return render(request, 'server/detail_seg.html', {'item': item})


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


login_required(redirect_field_name=None, login_url='/')


def segment(request):
    scan_segment = SegmentScan.objects.all()
    error = ''
    if request.method == 'POST':
        form = SegmentScanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('segment')
        else:
            error = 'Форма не верна'
    form_segment = SegmentScanForm()
    seg = {
        'form_segment': form_segment,
        'error': error,
        'scan_segment': scan_segment,
    }
    return render(request, 'server/segment.html', seg)
