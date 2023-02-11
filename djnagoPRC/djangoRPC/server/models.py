from django.db import models

class DataPorts(models.Model):
    data = models.CharField(max_length=100)

class DataServer(models.Model):
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    
