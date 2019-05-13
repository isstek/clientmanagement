from django import forms
from django.conf import settings
import collections, copy
from clientmanagement import views as main_views
from django.urls import reverse
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime
from models import tools
from clientmanagement.widget import form_switch

class FileToolForm(forms.ModelForm):
    order = ("name", "public", "version", "uplfile", "description")
    inf_page_title = "Add file tool: CMS infotek"
    inf_subm_button = "Submit"
    inf_action='add'
    inf_minititle = 'Add a file tool'
    inf_delete_button = False

    public = form_switch.SwitchOnOffField(label="Public link?", required=False)
    class Meta:
        model = tools.FileTool
        fields = ("name", "public", "version", "uplfile", "description")

    def __init__(self, *args, **kwargs): 
        form = super(FileToolForm, self).__init__(*args, **kwargs) 
        self.fields['public'].label_classes = ('switch-paddle', 'class_b', )
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.inf_page_title = "Change file tool: CMS infotek"
            self.inf_action='changed'
            self.inf_minititle = 'Change the file tool'
            self.inf_delete_button = "Delete tool"
            self.fields.pop('uplfile')

class LinkToolForm(forms.ModelForm):
    order = ("name", "public", "url", "description")
    inf_page_title = "Add link tool: CMS infotek"
    inf_subm_button = "Submit"
    inf_action='add'
    inf_minititle = 'Add a link to a tool'
    inf_delete_button = False

    public = form_switch.SwitchOnOffField(label="Public link?", required=False)
    class Meta:
        model = tools.LinkTool
        fields = ("name", "public", "url", "description")

    def __init__(self, *args, **kwargs): 
        super(LinkToolForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.inf_page_title = "Change link tool: CMS infotek"
            self.inf_action='changed'
            self.inf_minititle = 'Change a link to a tool'
            self.inf_delete_button = "Delete tool"
            


def ToolFormParser(request, form_type):    
    valid, response = main_views.initRequest(request)
    if not valid:
        return response
    data={}
    back_link = reverse('all_tools', kwargs={'tool_type':''})
    if (form_type == 'f'):
        form_class = FileToolForm
        obj_class = tools.FileTool
    if (form_type == 'l'):
        form_class = LinkToolForm
        obj_class = tools.LinkTool
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action']=='add'):
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(back_link)
        elif (request.POST['action']=='change'):
            if('targetid' in request.POST):
                try:
                    curobj=obj_class.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(back_link)
            form = form_class(instance=curobj)
        elif (request.POST['action']=='changed'):
            if('targetid' in request.POST):
                try:
                    curobj=obj_class.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(back_link)
            form = form_class(request.POST, request.FILES, instance=curobj)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                return redirect(back_link)
        elif (request.POST['action']=='delete'):
            if('targetid' in request.POST):
                try:
                    curobj=obj_class.objects.get(id=request.POST['targetid'])
                except Exception:
                    return redirect(back_link)
            curobj.delete()
            return redirect(back_link)
        else:
            return redirect(back_link)
    else:
        form = form_class()
    data['PAGE_TITLE'] = form.inf_page_title
    data['action'] = form.inf_action
    data['minititle'] = form.inf_minititle
    data['submbutton'] = form.inf_subm_button
    data['deletebutton'] = form.inf_delete_button
    data['backurl'] = back_link
    if('targetid' in request.POST):
        data['targetid'] = request.POST['targetid']
    data['form'] = form
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'forms/unimodelform.html', data, content_type='text/html')
