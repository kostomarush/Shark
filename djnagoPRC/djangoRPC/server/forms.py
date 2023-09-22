from .models import DataServer, SegmentScan
from django.forms import ModelForm, TextInput

class DataServerForm(ModelForm):
    class Meta:
        model = DataServer
        fields = ['ip', 'port', 'mode']

        widgets = {
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ip address',
            }),
            'port': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Port',

            }),
            'mode': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mode',

            })
            
        }

class SegmentScanForm(ModelForm):
    class Meta:
        model = SegmentScan
        fields = ['ip', 'mask', 'mode']

        widgets = {
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ip address',
            }),
            'mask': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mask',

            }),
            'mode': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mode',

            })
            
        }