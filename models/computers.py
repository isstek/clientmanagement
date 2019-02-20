from django.db import models
from models import description
from models import networkequipment
from models import person
from models import client

class Computer(description.Description):
    OPERATING_SYSTEMS = (
        ('W10', 'Windows 10'),
        ('W7', 'Windows 7'),
        ('WXP', 'Windows XP'),
        ('WO', 'Windows Other'),
        ('MHS', 'MacOS High Siera')
    )
    computername = models.CharField('Computer Name', max_length=30, null=False)
    operatingsystem = models.CharField(max_length=3, null=True, default='NULL')
    user = models.ManyToManyField(client.Client)
