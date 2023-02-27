from .models import DataServer
from django.forms import ModelForm, TextInput

class DataServerForm(ModelForm):
    class Meta:
        model = DataServer
        fields = ['ip', 'port']

        widgets = {
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ip address',
            }),
            'port': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Port',

            })
        }