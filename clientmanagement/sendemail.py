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

def sendemailtoone(template, data, subject, email, name):
    plaintext = get_template(template)
    data['name'] = name
    text_content = plaintext.render(data)
    msg = EmailMultiAlternatives(subject, text_content, '', [email])
    msg.send()

def sendemailtosome(template, data, subject, email):
    plaintext = get_template(template)
    text_content = plaintext.render(data)
    msg = EmailMultiAlternatives(subject, text_content, '', email)
    msg.send()

def sendemailtouser(template, data, subject, user):
    plaintext = get_template(template)
    data['useer'] = user
    text_content = plaintext.render(data)
    msg = EmailMultiAlternatives(subject, text_content, '', [user.email])
    msg.send()