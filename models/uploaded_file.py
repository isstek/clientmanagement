from django.db import models
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.urls import reverse
import pytz, uuid, os
from models import ticket, ticket_comment


class UploadedFileTicket(models.Model):
    for_ticket = models.ForeignKey(ticket.Ticket, on_delete=models.CASCADE, null=False)
    createdon = models.DateTimeField("Created time", auto_now_add=True, null=False, blank=False)
    uplfile = models.FileField(upload_to=file_location, max_length=255)

    def createtime(self):
        return self.createdon.astimezone(pytz.timezone('America/New_York'))

    def closetime(self):
        return self.resolvedon.astimezone(pytz.timezone('America/New_York'))
    
    def __str__(self):
        return "Ticket number " + str(self.id)

    def file_location(self):
        return os.path.join(settings.TICKET_FILES, self.for_ticket.id)
