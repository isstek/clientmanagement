from django import forms
from models import client
from clientmanagement import views as main_views
from django.urls import reverse
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime

class ClientForm(forms.ModelForm):

    class Meta:
        model = client.Client
        fields = ('name', 'address', 'phone', 'description')


def ClientFormParse(request):
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    data={}
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = ClientForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('oneclient', kwargs={'clientid': model.id}))
            else:
                data['action'] = 'add'
                data['minititle'] = 'New Client'
                data['submbutton'] = 'Add client'
                data['PAGE_TITLE'] = 'New Client: CMS infotek'
                data['backurl'] = reverse('allclients')
        elif (request.POST['action']=='change'):
            if('targetid' in request.POST):
                try:
                    curcl=client.Client.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('allclients'))
                form = ClientForm(instance=curcl)
                data['action'] = 'changed'
                data['targetid'] = request.POST['targetid']
                data['minititle'] = 'Change Client "'+curcl.name+'"'
                data['submbutton'] = 'Change client'
                data['backurl'] = reverse('oneclient', kwargs={'clientid': curcl.id})
                data['deletebutton'] = 'Delete client'
            else:
                return redirect(reverse('allclients'))
        elif (request.POST['action']=='changed'):
            if('targetid' in request.POST):
                try:
                    curcl=client.Client.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('allclients'))
                form = ClientForm(request.POST, instance=curcl)
                if form.is_valid():
                    model = form.save(commit=False)
                    model.save()
                    return redirect(reverse('oneclient', kwargs={'clientid': model.id}))
                data['backurl'] = reverse('oneclient', kwargs={'clientid': curcl.id})
                data['action'] = 'changed'
                data['targetid'] = request.POST['targetid']
                data['minititle'] = 'Change Client "'+curcl.name+'"'
                data['submbutton'] = 'Change client'
                data['PAGE_TITLE'] = 'Change Client: CMS infotek'
            else:
                return redirect(reverse('allclients'))
        elif (request.POST['action']=='delete'):
            if('targetid' in request.POST):
                try:
                    curcl=client.Client.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('allclients'))
                curcl.delete()
                return redirect(reverse('allclients'))
            else:
                return redirect(reverse('allclients'))
        else:
            return redirect(reverse('allclients'))
    else:
        form = ClientForm()
        data['action']='add'
        data['minititle'] = 'New Client'
        data['submbutton'] = 'Add client'
        data['PAGE_TITLE'] = 'New Client: CMS infotek'
        data['backurl'] = reverse('allclients')
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')