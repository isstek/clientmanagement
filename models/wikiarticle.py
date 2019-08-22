from django.db import models
from django.shortcuts import reverse
from datetime import datetime, timedelta, timezone
from clientmanagement import sendemail
from django.conf import settings
from clientmanagement.widget import quill
import pytz, uuid


def time_now(instance=None):
    return datetime.now(pytz.utc)

class Keywords(models.Model):
    word = models.CharField('Word', max_length=120, null=False, blank=False)

class WikiArticle(models.Model):
    postedon = models.DateTimeField('Creation time', default=time_now, null=False, blank=False)
    updatedon = models.DateTimeField('Update time', default=time_now, null=False, blank=False)
    title = models.CharField('Title', default='', max_length=160, null=False, blank=False)
    keywords = models.ManyToManyField("Keywords", verbose_name="Keywords")
    unid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    article = models.TextField('Wiki article')
    
    def __str__(self):
        return 'Wiki article: ' + self.title

    def editable(self):
        return True
    
    def get_quill_object(self):
        return quill.QuillObject(self.article)

    def get_link(self):
        return reverse("wiki_art", kwargs={"wikiuuid": self.unid})

    def createdon(self):
        return self.updatedon

