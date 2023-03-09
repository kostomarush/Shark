from django.db import models

class ScanInfo(models.Model):
    ip_status = models.CharField(max_length=20)
    protocols = models.CharField(max_length=20)
    open_ports = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    os_detection = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    os_family = models.CharField(max_length=20)
    osgen = models.CharField(max_length=20)


class ClientBD(models.Model):
    ip_client = models.CharField(max_length=20)

    def __str__(self):
        return self.ip_client

class DataServer(models.Model):
    client = models.OneToOneField(ClientBD, on_delete=models.SET_NULL, null=True)
    tag = models.BooleanField(default=False)
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    mode = models.CharField(max_length=20)
