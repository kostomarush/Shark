from django.db import models

class DataPorts(models.Model):
    info_scan = models.CharField(max_length=1000)

class DataServer(models.Model):
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    
