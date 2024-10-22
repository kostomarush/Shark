from django.db import models


class ClientBD(models.Model):
    
    ip_client = models.CharField(max_length=20)

    def __str__(self):
        return self.ip_client

class DataServer(models.Model):
    
    MODE_CHOICES = (
        ('', 'Выберите режим'), 
        ('TCP', 'TCP'),
        ('UDP', 'UDP'),
        ('OS', 'OS')
    )
    
    tag = models.CharField(max_length=10, default=False)
    ip = models.CharField(max_length=20)
    port = models.CharField(max_length=20, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='')
    client = models.ForeignKey(ClientBD, on_delete=models.SET_NULL, null=True)
    cve_report = models.BooleanField(default=False)
    

class ScanInfo(models.Model):
    host = models.CharField(max_length=20)
    state_scan = models.CharField(max_length=20)
    state_ports = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=40)
    osfamily = models.CharField(max_length=100)
    osgen = models.CharField(max_length=100)
    accuracy = models.CharField(max_length=20)
    result = models.ForeignKey(
        DataServer, on_delete=models.CASCADE)
    
    is_execution_complete = models.BooleanField(default=False)

    def mark_execution_complete(self):
        self.is_execution_complete = True
        self.save()
    

class ResultPortsAim(models.Model):
    port = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    service = models.CharField(max_length=20)
    one_cve = models.TextField()
    all_info = models.ForeignKey(ScanInfo, on_delete=models.CASCADE)


class SegmentScan(models.Model):

    MODE_CHOICES = (
        ('', 'Выберите режим'), 
        ('TCP', 'TCP'),
        ('UDP', 'UDP'),
        ('OS', 'OS')
    )
    
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='')
    ip = models.CharField(max_length=20)
    mask = models.CharField(max_length=20)
    state_scan = models.CharField(max_length=20, default=False)
    cve_report = models.BooleanField(default=False)
    full_scan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    


class IPAddress(models.Model):
    address = models.GenericIPAddressField()
    client = models.ForeignKey(
        ClientBD, on_delete=models.SET_NULL, null=True)
    tag = models.CharField(max_length=20, default=False)
    seg_scan = models.ForeignKey(SegmentScan, on_delete=models.CASCADE)


class SegmentResult(models.Model):
    host = models.CharField(max_length=20)
    state_scan = models.CharField(max_length=20)
    state_ports = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    osfamily = models.CharField(max_length=100)
    osgen = models.CharField(max_length=100)
    accuracy = models.CharField(max_length=20)
    result = models.ForeignKey(
        IPAddress, on_delete=models.CASCADE)
    
    is_execution_complete = models.BooleanField(default=False)

    def mark_execution_complete(self):
        self.is_execution_complete = True
        self.save()
        


class ResultPorts(models.Model):
    port = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    service = models.CharField(max_length=20)
    one_cve = models.TextField()
    all_info = models.ForeignKey(SegmentResult, on_delete=models.CASCADE)

class CveInformation(models.Model):
    cve_information = models.TextField()
    result_ports = models.ForeignKey(ResultPorts, on_delete=models.CASCADE)

class LevelCve(models.Model):
    
    is_execution_complete = models.BooleanField(default=False)

    def mark_execution_complete(self):
        self.is_execution_complete = True
        self.save()
        
    port = models.CharField(max_length=10)
    cve = models.CharField(max_length=20)
    level = models.CharField(max_length=30)
    year = models.CharField(max_length=10)
    result = models.ForeignKey(SegmentResult, on_delete=models.CASCADE)

class CveInformationAim(models.Model):
    cve_information = models.TextField()
    result_ports = models.ForeignKey(ResultPortsAim, on_delete=models.CASCADE)
    
class LevelCveAim(models.Model):
    port = models.CharField(max_length=10)
    cve = models.CharField(max_length=20)
    level = models.CharField(max_length=30)
    result = models.ForeignKey(ScanInfo, on_delete=models.CASCADE)
    

# class ResultOs(models.Model):
#     full_name = models.CharField(max_length=30)
#     vendor = models.CharField(max_length=20)
#     osfamily = models.CharField(max_length=20)
#     osgen = models.CharField(max_length=20)
#     accuracy = models.CharField(max_length=20)
#     result = models.ForeignKey(DataServer, on_delete=models.CASCADE)

