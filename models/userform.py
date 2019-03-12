from django import forms
from django.contrib.auth.models import User
from clientmanagement import views as main_views
from clientmanagement import userfunctions
from django.urls import reverse
from django.shortcuts import render, render_to_response, redirect

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

class UserShortForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')


def routerFormParse(request):    
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    data={}
    data['PAGE_TITLE'] = 'Change User: CMS infotek'
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = UserForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('clientmanagement'))
            else:
                data['action']='add'
                data['PAGE_TITLE'] = 'New User: CMS infotek'
                data['minititle'] = 'Add User'
                data['submbutton'] = 'Add user'
        elif (request.POST['action']=='change'):
            if('targetid' in request.POST):
                try:
                    curuser=userfunctions.getUser(request.POST['targetid'])
                except Exception:
                    return redirect(reverse('usermanagement'))
                form = UserShortForm(instance=curuser)
                data['action'] = 'changed'
                data['targetid'] = request.POST['targetid']
                data['minititle'] = 'Change User "'+curuser.full+'"'
                data['submbutton'] = 'Change printer'
                data['deletebutton'] = 'Delete ' +curprinter.printername
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        elif (request.POST['action']=='changed'):
            if('targetid' in request.POST):
                try:
                    curprinter=printer.Printer.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                form = PrinterFullForm(request.POST, instance=curprinter)
                if form.is_valid():
                    model = form.save(commit=False)
                    model.save()
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                data['action'] = 'changed'
                data['targetid'] = request.POST['targetid']
                data['minititle'] = 'Change Printer "'+curprinter.printername+'"'
                data['submbutton'] = 'Change printer'
                data['deletebutton'] = 'Delete ' +curprinter.printername
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        elif (request.POST['action']=='delete'): 
            if('targetid' in request.POST):
                try:
                    curprinter=printer.Printer.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
                curprinter.delete()
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
            else:
                return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
        else:
            return redirect(reverse('oneclient', kwargs={'clientid': clientid}))
    else:
        form = PrinterForm(initial={'company': b})
        data['action']='add'
        data['PAGE_TITLE'] = 'New Printer: CMS infotek'
        data['minititle'] = 'Add printer'
        data['submbutton'] = 'Add printer'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    data['backurl'] = reverse('oneclient', kwargs={'clientid': clientid})
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')