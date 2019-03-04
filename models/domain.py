from django.db import models
from models import computers
from models import client

from io import StringIO

class Domain(models.Model):
    server = models.ForeignKey(computers.Computer, on_delete=models.SET_NULL, related_name='domain', verbose_name='Domain server: ', null=True, blank=True, default=None)
    company = models.ForeignKey(client.Client, on_delete=models.CASCADE, related_name='domain', verbose_name='Company: ', null=False, blank=False, default=None)
    domainnameshort = models.CharField('Short domain name:', max_length=30, null=False, blank=False)
    domainnamelong = models.CharField('Long domain name (.local):', max_length=50, null=False, blank=False)
    admin = models.CharField('Domain admin username:', null=False, max_length=15, blank=False, default='administrator')
    dnsip = models.GenericIPAddressField('Domain dns IP: ', protocol='IPv4', null=False, blank=False, default='192.168.0.10')
    description = models.TextField('Description: ', blank=True, null=True, default='')

    def DomainLoginFile(self):
        resultfile = StringIO()
        resultfile.write('@echo off\n')
        resultfile.write('set /p pass=Enter domain admin password-> \n')
        resultfile.write('wmic.exe /interactive:off ComputerSystem Where "Name=\'%computername%\'" Call UnJoinDomainOrWorkgroup FUnjoinOptions=0\n')
        resultfile.write('wmic.exe /interactive:off ComputerSystem Where name="%computername%" call JoinDomainOrWorkgroup FJoinOptions=3 Name="' + self.domainnamelong + '" UserName="' + self.domainnameshort + '\\' + self.admin + '" Password="%pass%"\n')
        resultfile.write('pause')
        return {'file': resultfile, 'filename': 'join'+self.domainnameshort+'.bat'}


def checkUnique(client):
    try:
        domains = Domain.objects.filter(company=client)
        for d in domains:
            d.delete()
    except Exception as a:
        pass
    return True

def getDomain(client):
    try:
        domains = Domain.objects.filter(company=client)
        return domains[0]
    except Exception as a:
        pass
    return None
