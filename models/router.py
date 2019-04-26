from django.db import models
from datetime import datetime
from models import networkequipment
from django.core.validators import MaxValueValidator, MinValueValidator
from models import client

class Router(networkequipment.NetworkEquipment):
    MANUFACTURER = (
        ('S', 'Sonicwall'),
        ('N', 'Netgear'),
        ('A', 'Asus'),
        ('L', 'Linksys'),
        ('C', 'Cisco'),
        ('U', 'Ubiquity'),
        ('T', 'TP Link'),
        ('O', 'Other')
    )
    manufacturer = models.CharField(max_length=1, null=False, default='S', blank=False, choices=MANUFACTURER)
    model = models.CharField(max_length=40, null=True, default='', blank=True)
    serialnumber = models.CharField(max_length=50, null=True, default='', blank=True)
    externalip = models.GenericIPAddressField(verbose_name="External IP address", protocol='IPv4', null=True, blank=True, default='')
    settingslink = models.CharField("Link to settings", max_length=130, null=True, blank=True, default='')
    firmwareversion = models.CharField("Firware version", max_length=60, null=True, blank=True, default='')

    
    def __str__(self):
        return 'Router ' + self.manufacturer + ' ' + self.model


def checkUnique(client):
    try:
        routers = Router.objects.filter(company=client)
        for r in routers:
            r.delete()
    except Exception as a:
        pass
    return True

def getRouter(client):
    try:
        routers = Router.objects.filter(company=client)
        return routers[0]
    except Exception as a:
        pass
    return None
