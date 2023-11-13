from django.contrib import admin
from .models import DataServer, ClientBD, IPAddress, SegmentScan, SegmentResult, ScanInfo, ResultPorts, CveInformationAim, LevelCveAim, LevelCve

# Register your models here.
admin.site.register(DataServer)
admin.site.register(ClientBD)
admin.site.register(IPAddress)
admin.site.register(SegmentScan)
admin.site.register(SegmentResult)
admin.site.register(ScanInfo)
admin.site.register(ResultPorts)
admin.site.register(CveInformationAim)
admin.site.register(LevelCve)