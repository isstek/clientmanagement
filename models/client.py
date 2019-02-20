from django.db import models
from models import description
from models import person

class Client(description.Description):
    name = models.CharField('Client Name', max_length=40, null=False)
    address = models.CharField('Client Address', max_length=120, null=True, default='NULL')
    phone = models.CharField('Phone Number', max_length=20, null=True, default='NULL')
    employees = models.ManyToManyField(person.Person, through='WorksAt')

class WorksAt(models.Model):
    person = models.ForeignKey(person.Person, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    maincontact = models.BooleanField('Main Contact?', null=False, default='FALSE')