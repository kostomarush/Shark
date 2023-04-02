from django.shortcuts import render, redirect
from .models import ScanInfo, DataServer
from .forms import DataServerForm
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required



@login_required(redirect_field_name=None, login_url='/')
def remove_item(request, pk):
    item = DataServer.objects.get(pk=pk)
    item.delete()
    return redirect('index')

@login_required(redirect_field_name=None, login_url='/')
def get_json(request):
    open = ScanInfo.objects.filter(state='open').count()
    filtered = ScanInfo.objects.filter(state='filtered').count()
    close = ScanInfo.objects.filter(state='closed').count()
    open_filtered = ScanInfo.objects.filter(state='open|filtered').count()
    return JsonResponse([open,filtered,close,open_filtered], safe=False)

@login_required(redirect_field_name=None, login_url='/')
def get_client(request):
    client_1 = 0
    client_2 = 0
    data_server = DataServer.objects.in_bulk()
    for id in data_server:
        if data_server[id].tag=='Done' and data_server[id].client.id == '1':
            client_1+=1
        else:
            client_2+=1
    return JsonResponse([client_1,client_2], safe=False)


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
            return redirect('index')
        else:
            error = 'Форма не верна'
    form = DataServerForm()
    tasks = {
        'form': form,
        'data_serv': data_serv,
        'error': error,
        'section': query_results,
        'task_done': task_done,
        #'js_data': js_data,
    }
    return render(request, 'server/index.html', tasks)
