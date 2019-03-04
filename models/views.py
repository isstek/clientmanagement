from django.shortcuts import render
from clientmanagement import views as main_views
from urllib.parse import urlencode, urlparse, parse_qs
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render_to_response, redirect
from datetime import datetime
from django import forms

from models import clientform
from models import computerform
from models import printerform
from models import personform
from models import domainform
from models import routerform
from models import othernetequipform
# Create your views here.


def clientForm(request):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return clientform.ClientFormParse(request)


def personForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return personform.personFormParse(request, clientid)


def domainForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return domainform.domainFormParse(request, clientid)


def routerForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return routerform.routerFormParse(request, clientid)


def computerForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return computerform.computerFormParse(request, clientid)


def printerForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return printerform.printerFormParse(request, clientid)


def otherNetEquipmentForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    return othernetequipform.otherNetEquipFormParse(request, clientid)