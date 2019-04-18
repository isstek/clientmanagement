from django.db import models
from datetime import datetime, timedelta, timezone
from clientmanagement import sendemail
from django.conf import settings

class SystemUpdates(models.Model):
    
    version = models.CharField('Version', max_length=25, null=False, blank=False)
    postedon = models.DateTimeField('Update time', default=datetime.utcnow, null=False, blank=False)
    createdon = models.DateTimeField('Created time', auto_now_add=True, null=False, blank=False)
    author = models.CharField('Update author', max_length=80, null=True, blank=True)
    title = models.CharField('Title', max_length=120, null=False, blank=False)
    wassent = models.BooleanField('Was sent', null=False, blank=False, default=False)
    newstext = models.TextField('News in text format')
    
    def __str__(self):
        return 'Updates for ' + self.version

    def editable(self):
        if datetime.now(timezone.utc) - self.createdon > timedelta(minutes=settings.TIME_TO_EDIT):
            return False
        else:
            return True

    def sendemail(self):
        if (not self.wassent):
            self.wassent = True
            self.save()
            sendemail.sendemaileveryonetxt('emails/newpostemail.txt', {'post':self}, "New post: " + self.title)


def getCurrentVersion():
    try:
        latest_update = SystemUpdates.objects.all().order_by('-postedon')[0]
    except Exception:
        return "1.0.0"
    return latest_update.version