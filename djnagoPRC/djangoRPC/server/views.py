from django.shortcuts import render, redirect
from .models import ScanInfo, DataServer
from .forms import DataServerForm
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None, login_url='/')
def home(request):
    return render(request, 'server/home.html')
@login_required(redirect_field_name=None, login_url='/')
def data(request):
    query_results = ScanInfo.objects.all()
    data_serv = DataServer.objects.all()
    error = ''
    if request.method == 'POST':
        form = DataServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data')
        else:
            error = 'Форма не верна'
    form = DataServerForm()
    data = {
        'form': form,
        'section': query_results,
        'data_serv': data_serv,
        'error': error
    }
    return render(request, 'server/data.html', data)

