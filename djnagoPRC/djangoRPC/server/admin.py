from django.contrib import admin
from .models import DataServer, ClientBD, IPAddress, SegmentScan, SegmentResult, ScanInfo

# Register your models here.
admin.site.register(DataServer)
admin.site.register(ClientBD)
admin.site.register(IPAddress)
admin.site.register(SegmentScan)
admin.site.register(SegmentResult)
admin.site.register(ScanInfo)
