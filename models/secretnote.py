from django.db import models
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote, unquote
import pytz, uuid
from clientmanagement import sendemail
from clientmanagement.widget import quill


def calc_date():
    return datetime.today().date() + timedelta(days=7)

class SecretNote(models.Model):
    contactemail = models.EmailField("Contact email address*", max_length=120, null=True, blank=True)
    subject = models.CharField("Subject*", max_length=150, null=False, blank=False)
    note_text = models.TextField("Secret note text*", null=True, blank=True)
    createdon = models.DateTimeField("Created time", auto_now_add=True, null=False, blank=False)
    expireon = models.DateField("Note expires on", null=True, blank=True, default=calc_date)
    reads_max = models.IntegerField("Maximum number of reads left", null=True, blank=True, default=1)
    reads_used = models.IntegerField("Number of reads used", null=True, blank=True, default=0)
    unid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def reads_left(self):
        return self.reads_max - self.reads_used

    def createtime(self):
        return self.createdon.astimezone(pytz.timezone('America/New_York'))

    def expiretime(self):
        return self.expireon
    
    def __str__(self):
        return "Secret note number " + str(self.id)

    def sendemail(self):
        sendemail.sendemailhtml('emails/secret_note_created_email.htm', {"note": self}, 
            'New secret note', self.contactemail)
        
    def generate_link_external_close(self):
        return settings.EMAIL_HOST_LINK + reverse('note_close', kwargs={'noteuuid': self.unid})
        
    def generate_link_external_open(self):
        return settings.EMAIL_HOST_LINK + reverse('note_open', kwargs={'noteuuid': self.unid})
        
    def generate_link_internal(self):
        return settings.EMAIL_HOST_LINK + reverse('note_internal', kwargs={'noteid': self.id})

    def get_email_link(self):
        return "mailto:" + self.contactemail + "?subject=" + quote(self.subject)

    def expires(self):
        return not self.expireon is None

    def viewlimited(self):
        return not self.reads_max is None

    def expired(self):
        return (not self.expireon is None) and (self.expireon < datetime.today().date())

    def out_of_reads(self):
        return (not self.reads_max is None) and (self.reads_max <= self.reads_used)

    def is_available(self):
        return (self.expireon is None or (self.expireon >= datetime.today().date())) and (self.reads_max is None or self.reads_max > self.reads_used)

    def text(self):
        if self.is_available():
            result = self.note_text
            if (self.viewlimited()):
                self.reads_used = self.reads_used + 1
                self.save()
            if not self.is_available():
                self.close()
            return result
        else:
            self.close()
            return ""

    def text_internal(self):
        if self.is_available():
            result = self.note_text
            return result
        else:
            self.close()
            return ""
    
    def get_internal_object(self):
        return quill.QuillObject(self.text_internal())
    
    def get_external_object(self):
        return quill.QuillObject(self.text())

    def close(self):
        self.note_text = None
        self.save()
        return True
