from django.shortcuts import render
from server.models import ScanInfo
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None, login_url='/')
def home(request):
    return render(request, 'server/home.html')
@login_required(redirect_field_name=None, login_url='/')
def data(request):
    query_results = ScanInfo.objects.all()
    return render(request, 'server/data.html', {'section': query_results})