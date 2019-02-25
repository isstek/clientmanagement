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
from models import client
from models import computers
# Create your views here.


def clientForm(request):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    data={}
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = clientform.ClientForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('oneclient', kwargs={'clientid': model.id}))
            else:
                data['action'] = 'add'
                data['minititle'] = 'New Client'
                data['submbutton'] = 'Add client'
        elif (request.POST['action']=='change'):
            if('clid' in request.POST):
                try:
                    curcl=client.Client.objects.get(id=request.POST['clid'])
                except Exception:
                    return redirect(reverse('allclients'))
                form = clientform.ClientForm(instance=curcl)
                data['action'] = 'changed'
                data['clid'] = request.POST['clid']
                data['minititle'] = 'Change Client "'+curcl.name+'"'
                data['submbutton'] = 'Change client'
            else:
                return redirect(reverse('allclients'))
        elif (request.POST['action']=='changed'):
            if('clid' in request.POST):
                try:
                    curcl=client.Client.objects.get(id=request.POST['clid'])
                except Exception:
                    return redirect(reverse('allclients'))
                form = clientform.ClientForm(request.POST, instance=curcl)
                if form.is_valid():
                    model = form.save(commit=False)
                    model.save()
                    return redirect(reverse('oneclient', kwargs={'clientid': model.id}))
                data['action'] = 'changed'
                data['clid'] = request.POST['clid']
                data['minititle'] = 'Change Client "'+curcl.name+'"'
                data['submbutton'] = 'Change client'
            else:
                return redirect(reverse('allclients'))
        else:
            return redirect(reverse('allclients'))
    else:
        form = clientform.ClientForm()
        data['action']='add'
        data['minititle'] = 'New Client'
        data['submbutton'] = 'Add client'
    data['form'] = form
    data['PAGE_TITLE'] = 'New Client: CMS infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'forms/client.html', data, content_type='text/html')


def computerForm(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    data={}
    data['PAGE_TITLE'] = 'Change Computer: CMS infotek'
    try:
        b=client.Client.objects.get(id=clientid)
    except Exception as exc:
        return redirect(reverse('allclients'))
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = computerform.ComputerForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            else:
                data['action']='add'
        elif (request.POST['action']=='change'):
            if('compid' in request.POST):
                try:
                    curcomp=computers.Computer.objects.get(id=request.POST['compid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                form = computerform.ComputerForm(instance=curcomp)
                data['action'] = 'changed'
                data['compid'] = request.POST['compid']
                data['minititle'] = 'Change Computer "'+curcomp.computername+'"'
                data['submbutton'] = 'Change computer'
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        elif (request.POST['action']=='changed'):
            if('compid' in request.POST):
                try:
                    curcomp=computers.Computer.objects.get(id=request.POST['compid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                form = computerform.ComputerForm(request.POST)
                if form.is_valid():
                    model = form.save(commit=False)
                    model.save()
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                data['action'] = 'changed'
                data['compid'] = request.POST['compid']
                data['minititle'] = 'Change Computer "'+curcomp.computername+'"'
                data['submbutton'] = 'Change computer'
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        else:
            return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
    else:
        form = computerform.ComputerForm(initial={'company': b})
        data['action']='add'
        data['PAGE_TITLE'] = 'New Computer: CMS infotek'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    return render(request, 'forms/computer.html', data, content_type='text/html')