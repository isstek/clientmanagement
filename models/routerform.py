from django import forms
from models import router
from models import client
from clientmanagement import views as main_views
from django.urls import reverse
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime

class RouterForm(forms.ModelForm):

    class Meta:
        model = router.Router
        fields = ('manufacturer', 'model', 'serialnumber', 'firmwareversion', 'settingslink', 'externalip','connection_type', 'ip_type', 'ip_address', 'mac_address', 'company', 'description')


def routerFormParse(request, clientid):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    data={}
    data['PAGE_TITLE'] = 'Change Router: CMS infotek'
    try:
        b=client.Client.objects.get(id=clientid)
    except Exception as exc:
        return redirect(reverse('allclients'))
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = RouterForm(request.POST)
            if not router.checkUnique(b):
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            else:
                data['action']='add'
                data['PAGE_TITLE'] = 'New Router: CMS infotek'
                data['minititle'] = 'Add Router for '+b.name
                data['submbutton'] = 'Add router'
        elif (request.POST['action']=='change'):
            try:
                currouter = router.getRouter(b)
            except Exception:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            form = RouterForm(instance=currouter)
            data['action'] = 'changed'
            data['targetid'] = True
            data['deletebutton'] = 'Delete router for ' + b.name
            data['minititle'] = 'Change Router for "'+b.name+'"'
            data['submbutton'] = 'Change router'
        elif (request.POST['action']=='changed'):
            try:
                currouter = router.getRouter(b)
            except Exception:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            form = RouterForm(request.POST, instance=currouter)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            data['action'] = 'changed'
            data['targetid'] = True
            data['deletebutton'] = 'Delete router for ' + b.name
            data['minititle'] = 'Change Router for "'+b.name+'"'
            data['submbutton'] = 'Change router'
        elif (request.POST['action']=='delete'):
            try:
                currouter = router.getRouter(b)
            except Exception:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            currouter.delete()
            return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        else:
            return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
    else:
        form = RouterForm(initial={'company': b})
        data['action']='add'
        data['PAGE_TITLE'] = 'New Router: CMS infotek'
        data['minititle'] = 'Add Router for '+b.name
        data['submbutton'] = 'Add router'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    data['backurl'] = reverse('oneclient', kwargs={'clientid': clientid})
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')