from django.shortcuts import render
from server.models import DataPorts
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None, login_url='/')
def home(request):
    return render(request, 'server/home.html', {'section': 'home'})
@login_required(redirect_field_name=None, login_url='/')
def data(request):
    query_results = DataPorts.objects.all()
    return render(request, 'server/data.html', {'section': query_results})