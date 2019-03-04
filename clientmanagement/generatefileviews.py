from django.http import HttpResponse, FileResponse
from django.core.files.base import ContentFile
from django.urls import reverse
from django.shortcuts import redirect
from clientmanagement import views as main_views
from models import client
from models import domain
from clientmanagement import modelgetters

def downloadConnectDomainFile(request, clientid):
    valid, response = main_views.initRequestLogin(request)
    if not valid:
        return response
    try:
        cur_client = client.Client.objects.get(id=clientid)
    except Exception as err:
        return redirect(reverse('allclients'))
    cur_domain = domain.getDomain(cur_client)
    resfile = cur_domain.DomainLoginFile()
    response = HttpResponse(content_type='text/bat')
    response['Content-Disposition'] = 'attachment; filename="'+resfile['filename']+'"'
    response.write(resfile['file'].getvalue())
    return response
 