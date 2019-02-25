from django.db import models

class Description(models.Model):
    description = models.TextField('Additional information', null=True, default='', blank=True)

    def create(description=''):
        return Description(description=description)
        
    def __str__(self):
        return self.description