from django.db import models
from datetime import datetime, timedelta, timezone
import uuid
from clientmanagement import sendemail
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Ticket(models.Model):
    createdon = models.DateTimeField("Created time", auto_now_add=True, null=False, blank=False)
    companyname = models.CharField("Company name*", max_length=60, null=False, blank=False)
    contactname = models.CharField("Contact name*", max_length=120, null=False, blank=False)
    contactphone = PhoneNumberField("Contact phone number", help_text= "In the following format: +10000000000x0000, if you need extension")
    contactemail = models.EmailField("Contact email address*", max_length=120, null=False, blank=False)
    title = models.CharField("Subject*", max_length=120, null=False, blank=False)
    description = models.TextField("Description of the issue", null=True, blank=True)
    senderipaddress = models.GenericIPAddressField("Sender IP address")
    resolved = models.BooleanField("Issue resolved", null=False, blank=False, default=False)
    resolvedon = models.DateTimeField("Resolved on", null=True, blank=True, default=None)
    resolvedby = models.CharField("Resolved by", max_length=60, null=True, blank=True, default=None)
    unid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return "Ticket number " + str(self.id)

    def sendemail(self):
        sendemail.sendemaileveryonetxt("emails/newpostemail.txt", {"post":self}, "New post: " + self.title)

    def close(self, user):
        self.resolved = True
        self.resolvedon = datetime.now()
        if (user.is_authenticated):
            self.resolvedby = user.get_full_name()
        else:
            self.resolvedby = "Anonymous"
        self.save()
        return True

    def open(self):
        self.resolved = False
        self.resolvedon = None
        self.resolvedby = None
        self.save()
        return True