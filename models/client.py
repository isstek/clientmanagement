from django.db import models
from models import description

class Client(description.Description):
    name = models.CharField('Client Name', max_length=40, null=False)
    address = models.CharField('Client Address', max_length=120, null=True, default='', blank=True)
    phone = models.CharField('Phone Number', max_length=20, null=True, default='', blank=True)
    
    def __str__(self):
        return self.name