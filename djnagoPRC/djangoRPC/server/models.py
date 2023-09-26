from django.db import models


class ScanInfo(models.Model):
    ip_status = models.CharField(max_length=20)
    protocols = models.CharField(max_length=20)
    open_ports = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    data_chunk = models.TextField()


class ClientBD(models.Model):
    ip_client = models.CharField(max_length=20)

    def __str__(self):
        return self.ip_client

class IPAddress(models.Model):
    address = models.GenericIPAddressField()
    client = models.ForeignKey(ClientBD, on_delete=models.CASCADE, related_name='ip_addresses')

    


class DataServer(models.Model):
    client = models.ForeignKey(ClientBD, on_delete=models.SET_NULL, null=True)
    tag = models.CharField(max_length=10, default=False)
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    mode = models.CharField(max_length=20)


class SegmentScan(models.Model):
    ip = models.CharField(max_length=20)
    mask = models.CharField(max_length=20)
    mode = models.CharField(max_length=20)
    state_scan = models.CharField(max_length=20, default=False)



class SegmentResult(models.Model):
    state_scan = models.CharField(max_length=20, default=False)
    
