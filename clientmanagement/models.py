from django.db import models

class Client(models.Model):
    name = models.CharField('Client Name', max_length=40)
    address = models.CharField('Client Address', max_length=120)
    phone = models.CharField('Phone Number', max_length=20)
