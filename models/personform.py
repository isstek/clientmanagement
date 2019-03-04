from django import forms
from models import person
from models import computers
from models import client
from django.urls import reverse
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime

class PersonForm(forms.ModelForm):

    class Meta:
        model = person.Person
        fields = ('firstname', 'lastname', 'email', 'phone', 'annoyance', 'employedby', 'description')


class PersonFullForm(PersonForm):

    class Meta(PersonForm.Meta):
        fields = ('firstname', 'lastname', 'email', 'phone', 'annoyance', 'employedby', 'description')
 

def personFormParse(request, clientid):
    data={}
    data['PAGE_TITLE'] = 'Change Person: CMS infotek'
    try:
        b=client.Client.objects.get(id=clientid)
    except Exception as exc:
        return redirect(reverse('allclients'))
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = PersonForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            else:
                data['action']='add'
                data['PAGE_TITLE'] = 'New Person: CMS infotek'
                data['minititle'] = 'Add Person'
                data['submbutton'] = 'Add person'
        elif (request.POST['action']=='change'):
            if('targetid' in request.POST):
                try:
                    curpers=person.Person.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                form = PersonForm(instance=curpers)
                data['action'] = 'changed'
                data['targetid'] = request.POST['targetid']
                data['minititle'] = 'Change Person "'+curpers.name()+'"'
                data['submbutton'] = 'Change person'
                data['deletebutton'] = 'Delete ' +curpers.name()
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        elif (request.POST['action']=='changed'):
            if('targetid' in request.POST):
                try:
                    curpers=person.Person.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                form = PersonForm(request.POST, instance=curpers)
                if form.is_valid():
                    model = form.save(commit=False)
                    model.save()
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                data['action'] = 'changed'
                data['targetid'] = request.POST['targetid']
                data['minititle'] = 'Change Person "'+curpers.name()+'"'
                data['submbutton'] = 'Change person'
                data['deletebutton'] = 'Delete ' +curpers.name()
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        elif (request.POST['action']=='delete'):
            if('targetid' in request.POST):
                try:
                    curpers=person.Person.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                curpers.delete()
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        else:
            return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
    else:
        form = PersonForm(initial={'employedby': b})
        data['action']='add'
        data['PAGE_TITLE'] = 'New Person: CMS infotek'
        data['minititle'] = 'Add Person'
        data['submbutton'] = 'Add person'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    data['backurl'] = reverse('oneclient', kwargs={'clientid': clientid})
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')