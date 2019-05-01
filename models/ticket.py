from django.db import models
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.urls import reverse
import pytz, uuid, os
from clientmanagement import sendemail as emailsending
from phonenumber_field.modelfields import PhoneNumberField
from urllib.parse import quote, unquote
from django.core.files.storage import DefaultStorage
from django.contrib.auth.models import User


class Ticket(models.Model):
    createdon = models.DateTimeField("Created time", auto_now_add=True, null=False, blank=False)
    companyname = models.CharField("Company name*", max_length=90, null=False, blank=False)
    contactname = models.CharField("Contact name*", max_length=120, null=False, blank=False)
    contactphone = PhoneNumberField("Contact phone number", help_text= "In the following format: +10000000000x0000, if you need extension")
    contactemail = models.EmailField("Contact email address*", max_length=120, null=False, blank=False)
    title = models.CharField("Subject*", max_length=160, null=False, blank=False)
    description = models.TextField("Description of the issue", null=True, blank=True)
    senderipaddress = models.GenericIPAddressField("Sender IP address")
    resolved = models.BooleanField("Issue resolved", null=False, blank=False, default=False)
    resolvedon = models.DateTimeField("Resolved on", null=True, blank=True, default=None)
    resolvedby = models.CharField("Resolved by", max_length=120, null=True, blank=True, default=None)
    unid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    assignedto = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Assigned to", null=True, blank=True)

    def createtime(self):
        return self.createdon.astimezone(pytz.timezone('America/New_York'))

    def closetime(self):
        return self.resolvedon.astimezone(pytz.timezone('America/New_York'))
    
    def __str__(self):
        return "Ticket number " + str(self.id)

    def sendemail(self, autocreated=False):
        if settings.SEND_EMAILS_TEAM_ON_TICKET_CREATE_TO_SUPPORT:
            self.sendemailsupportteam()
        if settings.SEND_EMAILS_ON_NEW_TICKET_MANUAL and not autocreated or settings.SEND_EMAILS_ON_NEW_TICKET_CREATED_AUTOMATICALLY and autocreated:
            self.sendemailclient()

    def sendemailclient(self):
        emailsending.sendemailtoone('emails/ticket_confirmation_email.htm', {"ticket": self, 
            "link": self.generate_link(), "answerlink": self.generate_answer_link()}, 
            'New ticket submited to Infotek', self.contactemail, self.contactname)

    def sendemailsupportteam(self):
        emailsending.sendemailtosome('emails/ticket_creation_support_team_email.htm', {"ticket": self, 
            "link": self.generate_link()}, 'New ticket from ' + self.contactname, settings.SUPPORT_TEAM_EMAIL_RECIPIENT)

    def get_files_folder(self):
        folder_path = os.path.join(settings.TICKET_FILES, str(self.id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

       
    def generate_link(self):
        return settings.EMAIL_HOST_LINK + reverse('ticket_view_direct', kwargs={'ticketuuid': self.unid})

    def generate_answer_link(self):
        return False

    def get_email_link(self):
        return "mailto:" + self.contactemail + "?subject=" + quote(self.title)

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
