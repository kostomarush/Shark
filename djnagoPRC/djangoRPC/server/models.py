from django.db import models


class ScanInfo(models.Model):
    ip_status = models.CharField(max_length=20)
    protocols = models.CharField(max_length=20)
    open_ports = models.CharField(max_length=20)
    state = models.CharField(max_length=20)


class ClientBD(models.Model):
    ip_client = models.CharField(max_length=20)

    def __str__(self):
        return self.ip_client


class DataServer(models.Model):
    client = models.ForeignKey(ClientBD, on_delete=models.SET_NULL, null=True)
    tag = models.CharField(max_length=10, default=False)
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    mode = models.CharField(max_length=20)
