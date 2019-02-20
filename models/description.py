from django.db import models

class Description(models.Model):
    description = models.TextField('Additional information', null=False, default='')

    def create(description=''):
        return Description(description=description)