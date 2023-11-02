from .models import DataServer, SegmentScan
from django.forms import ModelForm, Select, TextInput, BooleanField, CheckboxInput

class DataServerForm(ModelForm):
    class Meta:
        model = DataServer
        fields = ['ip', 'port', 'mode', 'cve_report']

        widgets = {
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ip address',
            }),
            'port': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Port',

            }),
            'mode': Select(attrs={
                'class': 'form-control',

            })
            
        }

class SegmentScanForm(ModelForm):
    class Meta:
        model = SegmentScan
        fields = ['ip', 'mask', 'mode', 'cve_report', 'full_scan']

        widgets = {
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ip адрес',
            }),
            'mask': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Маска',

            }),
            'mode': Select(attrs={
                'class': 'form-control'
            })
        
        }