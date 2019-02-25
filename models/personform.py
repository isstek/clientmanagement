from django import forms
from models import person

class PersonForm(forms.ModelForm):

    class Meta:
        model = person.Person
        fields = ('firstname', 'lastname', 'email', 'phone', 'annoyance', 'description')
