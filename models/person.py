from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from models import client

class Person(models.Model):
    firstname = models.CharField('First Name', max_length=30)
    lastname = models.CharField('Last Name', max_length=30)
    email = models.EmailField('Email', max_length=254, null=True, blank=True)
    phone = models.CharField('Phone Number', max_length=20, null=True, blank=True, default='')
    annoyance = models.fields.PositiveSmallIntegerField('Annoyance level', null=False, default='0', validators=[MaxValueValidator(10), MinValueValidator(0)])
    employedby = models.ForeignKey(client.Client, verbose_name='Employed by', null=True, default='', blank=True, related_name='employees', on_delete=models.CASCADE)
    description = models.TextField('Additional information', null=True, default='', blank=True)

    def create(first='', last='', email='', phone=None, annoyance=0, description='', company=[]):
        person = Person(firstname=first, lastname=last, email=email, phone=phone, annoyance=annoyance)
        return Person()
    
    def name(self):
        return self.firstname + ' ' +self.lastname
    
    def __str__(self):
        return self.name()