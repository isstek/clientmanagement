from django import forms
from models import client

class ClientForm(forms.ModelForm):

    class Meta:
        model = client.Client
        fields = ('name', 'address', 'phone', 'description')
