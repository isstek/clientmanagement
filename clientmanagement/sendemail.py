from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User


def sendemaileveryonetxt(template, data, subject):
    plaintext = get_template(template)
    for user in User.objects.exclude(email__isnull=True).exclude(email__exact=''):
        data['user'] = user
        text_content = plaintext.render(data)
        msg = EmailMultiAlternatives(subject, text_content, '', [user.email])
        msg.send()
