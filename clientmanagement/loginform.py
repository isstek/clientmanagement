from django import forms
from django.conf import settings
from django.contrib.auth import views as auth_views
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


class MyLoginForm(forms.Form):
    username = forms.CharField(label='User name', required=True, error_messages={'required': 'Please enter your username', 
    'notfound': 'This combination of username and password was not found'})
    password = forms.CharField(label='Password', required=True, error_messages={'required': 'Please enter your username'}, widget=forms.PasswordInput)
    rcaptcha = ReCaptchaField(label='', required=True, error_messages={'required': 'Please, check the box to prove you are not a robot'}, widget=ReCaptchaV2Invisible)

    def process(self, request):
        user = userfunctions.loginUser(request, self.cleaned_data['username'], self.cleaned_data['password'])
        if user is None:
            self.add_error(self.username, 'notfound')
            return False, ''
        redirect_to = self.get_redirect_url(request)
        if redirect_to == request.path:
            redirect_to = '/'
        return True, redirect_to


    def get_redirect_url(self, request):
        redirect_to = request.GET.get('next', '/')
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=request.get_host(),
            require_https=request.is_secure(),
        )
        return redirect_to if url_is_safe else ''



def myLoginFormParse(request):
    data={}
    data['PAGE_TITLE'] = 'Login: CMS infotek'
    if (request.method == 'POST'):
        form = MyLoginForm(request.POST)
        if form.is_valid():
            result, url = form.process(request)
            if result:
                return redirect(url)
    else:
        form = MyLoginForm()
        data['action']='add'
        data['PAGE_TITLE'] = 'New Person: CMS infotek'
        data['minititle'] = 'Add Person'
        data['submbutton'] = 'Add person'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'registration/login.html', data, content_type='text/html')