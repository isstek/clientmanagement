from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.template import Context
from django.contrib.auth.models import User


def sendemaileveryone(template, data, subject):
    if template[-3:] == 'htm':
        sendemaileveryonehtml(template, data, subject)
    else:
        sendemaileveryonetxt(template, data, subject)

def sendemailtoone(template, data, subject, email, name):
    if template[-3:] == 'htm':
        sendemailtoonehtml(template, data, subject, email, name)
    else:
        sendemailtoonetxt(template, data, subject, email, name)

def sendemailtosome(template, data, subject, email):
    if template[-3:] == 'htm':
        sendemailtosomehtml(template, data, subject, email)
    else:
        sendemailtosometxt(template, data, subject, email)

def sendemailtouser(template, data, subject, user):
    if template[-3:] == 'htm':
        sendemailtouserhtml(template, data, subject, user)
    else:
        sendemailtousertxt(template, data, subject, user)


def sendemaileveryonetxt(template, data, subject):
    plaintext = get_template(template)
    for user in User.objects.exclude(email__isnull=True).exclude(email__exact=''):
        data['user'] = user
        text_content = plaintext.render(data)
        msg = EmailMultiAlternatives(subject, text_content, '', [user.email])
        msg.send()

def sendemailtoonetxt(template, data, subject, email, name):
    plaintext = get_template(template)
    data['name'] = name
    text_content = plaintext.render(data)
    msg = EmailMultiAlternatives(subject, text_content, '', [email])
    msg.send()

def sendemailtosometxt(template, data, subject, email):
    plaintext = get_template(template)
    text_content = plaintext.render(data)
    msg = EmailMultiAlternatives(subject, text_content, '', email)
    msg.send()

def sendemailtousertxt(template, data, subject, user):
    plaintext = get_template(template)
    data['user'] = user
    text_content = plaintext.render(data)
    msg = EmailMultiAlternatives(subject, text_content, '', [user.email])
    msg.send()


def sendemaileveryonehtml(template, data, subject):
    for user in User.objects.exclude(email__isnull=True).exclude(email__exact=''):
        data['user'] = user
        html_content = render_to_string(template, data)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, '', [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

def sendemailtoonehtml(template, data, subject, email, name):
    data['name'] = name
    html_content = render_to_string(template, data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, '', [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def sendemailtosomehtml(template, data, subject, email):
    html_content = render_to_string(template, data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, '', email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def sendemailtouserhtml(template, data, subject, user):
    data['user'] = user
    html_content = render_to_string(template, data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, '', [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def sendemailhtml(template, data, subject, email):
    html_content = render_to_string(template, data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, '', [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()