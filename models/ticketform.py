from django import forms
import collections, copy
from clientmanagement import modelgetters, sendemail
from clientmanagement import views as main_views
from django.urls import reverse
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime
from phonenumber_field.formfields import PhoneNumberField
from models import ticket
from django.contrib.sites.shortcuts import get_current_site


class TicketForm(forms.ModelForm):
    contactphone = PhoneNumberField(label="Contact phone number", required=False)
    class Meta:
        model = ticket.Ticket
        fields = ("title", "companyname", "contactname", "contactemail", "description")

    def __init__(self, *args, **kwargs): 
        super(TicketForm, self).__init__(*args, **kwargs)
        order = ("title", "companyname", "contactname", "contactemail", "contactphone", "description")
        tmp = self.fields
        self.fields = collections.OrderedDict()
        for item in order:
            self.fields[item] = tmp[item]

        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            if (not instance.contactphone is None) and (instance.contactphone != ""):
                self.fields['contactphone'].initial = instance.contactphone.as_national

    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)
        if ('contactphone' in self.changed_data):
            ticket.contactphone= self.cleaned_data["contactphone"]
        if commit:
            ticket.save()
        return ticket


def TicketFormParse(request):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    data={}
    data['PAGE_TITLE'] = 'Change posted update: CMS infotek'
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = TicketForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                model.senderipaddress = ip
                model.save()
                sendemail.sendemailtoone('emails/ticket_confirmation_email.txt', {"ticket": model, 
                "link": request.build_absolute_uri(reverse('ticket_view_direct', kwargs={'ticketuuid': model.unid}))}, 'New ticket submited to Infotek', model.contactemail, model.contactname)
                return redirect(reverse('ticket_submitted'))
            else:
                data['action']='add'
                data['PAGE_TITLE'] = 'Submit a ticket: CMS infotek'
                data['minititle'] = 'Submit a Ticket to Infotek'
                data['submbutton'] = 'Submit'
        else:
            return redirect(reverse('updates'))
    else:
        form = TicketForm()
        data['action']='add'
        data['PAGE_TITLE'] = 'Submit a ticket: CMS infotek'
        data['minititle'] = 'Submit a Ticket to Infotek'
        data['submbutton'] = 'Submit'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    data['backurl'] = reverse('updates')
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')


def TicketChangeFormParse(request, ticketid):  
    if not ticketid is None:
        try:
            curticket = ticket.Ticket.objects.get(id=ticketid)
        except Exception:
            return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
    else:
        return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
    data={}
    data['PAGE_TITLE'] = 'Change ticket update: CMS infotek'
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='close'):
            curticket.close(request.user)
            return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
        elif (request.POST['action']=='open'):
            curticket.open()
            return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
        elif (request.POST['action']=='change'):
            form = TicketForm(instance=curticket)
            data['action'] = 'changed'
            data['PAGE_TITLE'] = 'Change Ticket: CMS infotek'
            data['minititle'] = 'Change Ticket'
            data['submbutton'] = 'Change ticket'
            data['deletebutton'] = 'Delete ticket'
        elif (request.POST['action']=='changed'):
            form = TicketForm(request.POST, instance=curticket)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
            data['action'] = 'changed'
            data['PAGE_TITLE'] = 'Change Ticket: CMS infotek'
            data['minititle'] = 'Change Ticket'
            data['submbutton'] = 'Change ticket'
            data['deletebutton'] = 'Delete ticket'
        elif (request.POST['action']=='delete'):
            curticket.delete()
            return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
        else:
            return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
    else:
        form = TicketForm()
        data['action']='add'
        data['PAGE_TITLE'] = 'Submit a ticket: CMS infotek'
        data['minititle'] = 'Submit a Ticket to Infotek'
        data['submbutton'] = 'Submit'
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    data['backurl'] = reverse('alltickets', kwargs={'reqtype': 'o'})
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')


def ViewTicketDirectParse(request, ticketuuid):
    data = modelgetters.form_one_ticket_data(ticketuuid)
    if data is None:
        return redirect(reverse('alltickets', kwargs={'reqtype': 'o'}))
    data['can_change'] = request.user.is_authenticated
    data['built'] = datetime.now().strftime("%H:%M:%S") 
    data['PAGE_TITLE'] = 'Ticket View: CMS infotek'
    return render(request, 'views/ticketview.html', data, content_type='text/html')