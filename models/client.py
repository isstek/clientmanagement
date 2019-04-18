from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    name = models.CharField('Client Name', max_length=40, null=False)
    address = models.CharField('Client Address', max_length=120, null=True, default='', blank=True)
    phone = PhoneNumberField('Phone Number', help_text= "In the following format: +10000000000x0000, if you need extension", null=True, default=None, blank=True)
    description = models.TextField('Additional information', null=True, default='', blank=True)

    def __str__(self):
        return self.name