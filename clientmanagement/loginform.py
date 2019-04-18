from django import forms
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import forms as auth_forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
import collections, copy
from clientmanagement import userfunctions
from clientmanagement import views as main_views
from django.urls import reverse
from django.utils.http import is_safe_url
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime
from phonenumber_field.formfields import PhoneNumberField
from models import ticket, ticket_commentform
from django.contrib.sites.shortcuts import get_current_site

class MyAuthLoginForm(auth_forms.AuthenticationForm):
    rcaptcha = ReCaptchaField(label='', required=True, widget=ReCaptchaV2Invisible)


class my_reset_password_form(auth_forms.PasswordResetForm):
    rcaptcha = ReCaptchaField(label='', required=True, widget=ReCaptchaV2Invisible)