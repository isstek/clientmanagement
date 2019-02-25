from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from models import description
from models import client

class Person(description.Description):
    firstname = models.CharField('First Name', max_length=30)
    lastname = models.CharField('Last Name', max_length=30)
    email = models.EmailField('Email', max_length=254, null=True, blank=True)
    phone = models.CharField('Phone Number', max_length=20, null=True, blank=True, default='')
    annoyance = models.fields.PositiveSmallIntegerField('Annoyance level', null=False, default='0', validators=[MaxValueValidator(10), MinValueValidator(0)])
    employedby = models.ManyToManyField(client.Client, verbose_name='Employed by', through='WorksAt', related_name='employees')

    def create(first='', last='', email='', phone=None, annoyance=0, description='', company=[]):
        person = Person(firstname=first, lastname=last, email=email, phone=phone, annoyance=annoyance)
        return Person()
    
    def name(self):
        return self.firstname + ' ' +self.lastname
    
    def __str__(self):
        return self.name()

class WorksAt(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    client = models.ForeignKey(client.Client, on_delete=models.CASCADE)
    maincontact = models.BooleanField('Main Contact?', null=False, default=False)
