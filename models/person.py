from django.db import models
from models import description
from models import client

class Person(description.Description):
    firstname = models.CharField('First Name', max_length=30)
    lastname = models.CharField('Last Name', max_length=30)
    email = models.EmailField('Email', max_length=254)
    phone = models.CharField('Phone Number', max_length=20, null=True, default='NULL')
    annoyance = models.fields.PositiveSmallIntegerField('Annoyance level', null=False, default='0')

    def create(first='', last='', email='', phone=None, annoyance=0, description='', company=[]):
        person = Person(firstname=first, lastname=last, email=email, phone=phone, annoyance=annoyance)
        return Person()
