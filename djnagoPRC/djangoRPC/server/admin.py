from django.contrib import admin
from .models import DataServer, ClientBD, IPAddress, SegmentScan

# Register your models here.
admin.site.register(DataServer)
admin.site.register(ClientBD)
admin.site.register(IPAddress)
admin.site.register(SegmentScan)