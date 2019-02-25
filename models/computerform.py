from django import forms
from models import computers

class ComputerForm(forms.ModelForm):

    class Meta:
        model = computers.Computer
        fields = ('computername', 'operatingsystem', 'connection_type', 'ip_type', 'ip_address', 'mac_address', 'company', 'description')
