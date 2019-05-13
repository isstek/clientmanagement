from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.encoding import smart_str
from django.shortcuts import reverse
from django.dispatch import receiver
from django.conf import settings
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from datetime import datetime
from models import networkequipment, client
from clientmanagement import error_views, utilities
import os, mimetypes


def upload_to_router(instance, filename):
    return os.path.join(instance.get_file_folder(), filename)


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
    settings_file = models.FileField("Settings file", upload_to=upload_to_router, null=True, default=None, blank=True)
    settings_file_uploaded = models.DateField(null=True, default=None, blank=True)

    
    def __str__(self):
        return 'Router ' + self.manufacturer + ' ' + self.model

    def get_file_folder(self):
        folder_path = os.path.join(self.company.get_file_folder(), 'router')
        return folder_path

    def uploaded_on_text(self):
        return ' (Uploaded on ' + str(self.settings_file_uploaded) + ')'

    def settings_file_available(self):
        return self.settings_file is not None and self.settings_file and self.settings_file is not '' and os.path.exists(self.settings_file.path)

    def get_internal_link_to_settings(self):
        if self.settings_file_available():
            return reverse('download_router_settings', kwargs={'clientid': self.company.id})
        else:
            return None

    def get_link_text(self):
        if self.settings_file_available():
            return os.path.basename(self.settings_file.path) + self.uploaded_on_text() + ' (' + utilities.humanize_bytes(os.path.getsize(self.settings_file.path)) + ')'
        else:
            return None

    def get_link_to_settings(self):
        return settings.EMAIL_HOST_LINK + self.get_internal_link_to_file()

@receiver(models.signals.post_delete, sender=Router)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.settings_file:
        if os.path.isfile(instance.settings_file.path):
            os.remove(instance.settings_file.path)


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


def downloadSettingsFile(request, clientid):
    try:
        router = Router.objects.get(company_id=clientid)
    except Exception as exc:
        print(exc)
        return error_views.notfound(request)
    if not router.settings_file_available():
        return error_views.notfound(request)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(router.settings_file, chunk_size),
                            content_type=mimetypes.guess_type(router.settings_file.path)[0])
    response['Content-Length'] = os.path.getsize(router.settings_file.path)    
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(router.settings_file.path))
    return response
