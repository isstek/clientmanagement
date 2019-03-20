from django.shortcuts import render
from clientmanagement import views as main_views
from urllib.parse import urlencode, urlparse, parse_qs
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required 
from datetime import datetime
from django import forms

from models import clientform
from models import computerform
from models import printerform
from models import personform
from models import domainform
from models import routerform
from models import othernetequipform
from models import updatesform
from models import userform
from models import ticketform
# Create your views here.


@login_required( login_url = 'login' )
def clientForm(request):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return clientform.ClientFormParse(request)


@login_required( login_url = 'login' )
def personForm(request, clientid):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return personform.personFormParse(request, clientid)


@login_required( login_url = 'login' )
def domainForm(request, clientid):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return domainform.domainFormParse(request, clientid)


@login_required( login_url = 'login' )
def routerForm(request, clientid):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return routerform.routerFormParse(request, clientid)


@login_required( login_url = 'login' )
def computerForm(request, clientid):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return computerform.computerFormParse(request, clientid)


@login_required( login_url = 'login' )
def printerForm(request, clientid):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return printerform.printerFormParse(request, clientid)


@login_required( login_url = 'login' )
def otherNetEquipmentForm(request, clientid):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return othernetequipform.otherNetEquipFormParse(request, clientid)


@login_required( login_url = 'login' )
def PostSystemUpdate(request):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return updatesform.SystemUpdateFormParse(request)


@login_required( login_url = 'login' )
def addUserForm(request):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return userform.userFormParse(request)

@login_required( login_url = 'login' )
def changeTicketForm(request, ticketid=None):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return ticketform.TicketChangeFormParse(request, ticketid)


def submitTicketForm(request):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return ticketform.TicketFormParse(request)


def viewTicketDirectView(request, ticketuuid=None):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    return ticketform.ViewTicketDirectParse(request, ticketuuid)