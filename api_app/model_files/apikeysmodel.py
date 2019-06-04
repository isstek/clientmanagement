from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
import os, uuid, secrets, pytz

def expiration_date(instance=None):
    return datetime.today().date() + timedelta(days=settings.DEFAULT_API_EXPIRATION_PERIOD_DAYS)


class APIKey(models.Model):
    api_name = models.CharField('API Key name', max_length=40, null=True)
    secret_api_key = models.CharField('API Key', max_length=200, unique=True, null=False, blank=False)
    createdon = models.DateField('Created date', auto_now_add=True, null=False, blank=False)
    expireon = models.DateField('Expiration date', default=expiration_date, null=True, blank=True)
    description = models.TextField('Additional information', null=True, default='', blank=True)

    def expired(self):
        return datetime.today().date() > self.expireon

    @staticmethod
    def create_api_key(name=None, description=None):
        api_key = secrets.token_urlsafe(settings.DEFAULT_API_KEY_LENGTH)
        tries = 0
        if name is None:
            name = 'Created on ' + str(datetime.now())
        result = None
        while result is None:
            try:
                tries += 1
                result = APIKey.objects.create(api_name=name, secret_api_key=api_key, description=description)
                result.save()
            except Exception as e:
                print(e)
                result = None
                if tries == 10:
                    break
        return result

    @staticmethod
    def validate_api(api_secret):
        try:
            api_key = APIKey.objects.get(secret_api_key=api_secret)
        except Exception:
            return False, None
        if api_key is None or datetime.today().date()>api_key.expireon:
            return False, api_key
        return True, api_key

    def __str__(self):
        return self.api_name