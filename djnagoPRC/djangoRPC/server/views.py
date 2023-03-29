from django.shortcuts import render, redirect
from .models import ScanInfo, DataServer
from .forms import DataServerForm
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None, login_url='/')
def remove_item(request, pk):
    item = DataServer.objects.get(pk=pk)
    item.delete()
    return redirect('index')


@login_required(redirect_field_name=None, login_url='/')
def home(request):
    query_results = ScanInfo.objects.all()
    return render(request, 'server/index.html', {'section': query_results})

@login_required(redirect_field_name=None, login_url='/')
def data(request):
    query_results = ScanInfo.objects.all()
    data_serv = DataServer.objects.all()
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
    }
    return render(request, 'server/index.html', tasks)
