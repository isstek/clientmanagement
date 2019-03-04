from django.db import models
from models import client
from macaddress.fields import MACAddressField

class NetworkEquipment(models.Model):
    IP_TYPES=(
        ('N', 'No connection'),
        ('D', 'DHCP address'),
        ('L', 'Static address, local'),
        ('R', 'Static address, router'),
    )
    CONNECTION_TYPES=(
        ('N', 'No connection'),
        ('E', 'Ethernet'),
        ('W', 'WiFi'),
    )
    connection_type=models.CharField('Netowrk connection type', max_length=1, choices=CONNECTION_TYPES, default='N')
    ip_type = models.CharField('IP addressing type', max_length=1, choices=IP_TYPES, default='N')
    ip_address = models.GenericIPAddressField('IP Address', null=True, default='', blank=True)
    mac_address = MACAddressField(null=True, integer=False, blank=True)
    company = models.ForeignKey(client.Client, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField('Additional information', null=True, default='', blank=True)

    def __str__(self):
        return (('IP: '+self.ip_address + (('\nMAC: ' + self.mac_address) if (self.mac_address is not None) else ""))if (self.ip_address is not None) else (('MAC: ' + self.mac_address) if (self.mac_address is not None) else ""))
