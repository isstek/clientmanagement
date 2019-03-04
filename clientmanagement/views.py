"""
Core Django views for VAR project
"""
import json
import logging

from datetime import datetime
from urllib.parse import urlencode, urlparse, parse_qs
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render_to_response, redirect
from django.utils.cache import patch_response_headers
import os
from django.shortcuts import render
from django.conf import settings
from clientmanagement import userfunctions
from clientmanagement import modelgetters


# Get an instance of a logger
logger = logging.getLogger(__name__)


def initRequestLogin(request):
    if userfunctions.checkUser(request):
        return initRequest(request)
    else:
        return False, loginpage(request)


def initRequest(request):
    """
    A function to check and verify request
    :param request:
    :return:
    """

    url = request.get_full_path()
    u = urlparse(url)
    query = parse_qs(u.query)
    query.pop('timestamp', None)
    try:
        u = u._replace(query=urlencode(query, True))
    except UnicodeEncodeError:
        data = {
            'errormessage': 'Error appeared while encoding URL!'
        }
        return False, render_to_response(json.dumps(data), content_type='text/html')

    ## Set default page lifetime in the http header, for the use of the front end cache
    request.session['max_age_minutes'] = 10

    ## Create a dict in session for storing request params
    requestParams = {}
    request.session['requestParams'] = requestParams

    if request.method == 'POST':
        for p in request.POST:
            pval = request.POST[p]
            pval = pval.replace('+', ' ')
            request.session['requestParams'][p.lower()] = pval
    else:
        for p in request.GET:
            pval = request.GET[p]
            pval = pval.replace('+', ' ')

            ## Here check if int or date type params can be placed

            request.session['requestParams'][p.lower()] = pval

    return True, None


def homepage(request):
    valid, response = initRequestLogin(request)
    if not valid:
        return response
    data = {}
    data['PAGE_TITLE'] = 'CMS Infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'index.html', data, content_type='text/html')

def loginpage(request):
    valid, response = initRequest(request)
    if not valid:
        return response
    data = {}
    if (request.method == 'POST') and ('username' in request.POST) and ('password' in request.POST):
        try:
            user = userfunctions.loginUser(request, request.POST['username'], request.POST['password'])
            data['USER'] = user
            if ('last_URL' in request.POST):
                return redirect(request.POST['last_URL'])
            else:
                return redirect('/')
        except Exception as exc:
            logger.error('!views.loginpage!: Could not perform log in the client. \n' + str(exc))
    data['PAGE_TITLE'] = 'Login to CMS Infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'login.html', data, content_type='text/html')

def logout(request):
    valid, response = initRequest(request)
    if not valid:
        return response
    userfunctions.logoutUser(request)
    return redirect('/')


def usermanagement(request):
    valid, response = initRequestLogin(request)
    if not valid:
        return response
    data = {}
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action'] == 'deleteuser') and ('target' in request.POST):
            success, message = userfunctions.deleteUserID(request.POST['target'])
            data['success'] = success
            data['message'] = message
            data['username'] = request.POST['target']
            return JsonResponse(data)
    
    data['userlist'] = userfunctions.getUserList()
    data['PAGE_TITLE'] = 'Manage users: CMS infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'user/usermanagement.html', data, content_type='text/html')


def createuser(request):
    valid, response = initRequestLogin(request)
    if not valid:
        return response
    data = {}

    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action'] == 'validate') and ('target' in request.POST):
            if('value' in request.POST):
                if (request.POST['target']=='username'):
                    success, message = userfunctions.checkUsernameExists(request.POST['value'])
                    return JsonResponse({'success': success, 'message': message})
                elif(request.POST['target']=='email'):
                    success, message = userfunctions.checkEmailExists(request.POST['value'])
                    return JsonResponse({'success': success, 'message': message})
                elif(request.POST['target']=='password'):
                    success, message = userfunctions.checkPasswordComplexity(request.POST['value'])
                    return JsonResponse({'success': success, 'message': message})
                return JsonResponse({'success': False, 'message': 'Could not verify login'})
            else:
                return JsonResponse({'success': False, 'message': 'Could not verify login'})
        if (request.POST['action'] == 'createacc') and ('username' in request.POST) and ('password' in request.POST) and ('email' in request.POST) and \
                    ('firstname' in request.POST) and ('lastname' in request.POST):
            if (userfunctions.validateNewUser(request.POST['username'], request.POST['password'], request.POST['email'], request.POST['firstname'], request.POST['lastname'])):
                try:
                    user = userfunctions.createUser(request.POST['username'], request.POST['password'], request.POST['email'], request.POST['firstname'], request.POST['lastname'])
                    if user is not None:
                        return redirect('/usermanagement')
                except Exception as exc:
                    logger.error('!views.createuser!: Could not create user. \n' + str(exc))
            data['username']=request.POST['username']
            data['password']=request.POST['password']
            data['email']=request.POST['email']
            data['firstname']=request.POST['firstname']
            data['lastname']=request.POST['lastname']
            data['creationfailed']=True
            
    data['PAGE_TITLE'] = 'Create user: CMS Infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'user/createuser.html', data, content_type='text/html')


def changeuser(request):
    valid, response = initRequestLogin(request)
    if not valid:
        return response
    data = {}
    if (request.method == 'POST') and ('action' in request.POST):
        if (request.POST['action'] == 'validate') and ('target' in request.POST)and ('curusername' in request.POST):
            if('value' in request.POST):
                if (request.POST['target']=='username'):
                    success, message = userfunctions.checkUsernameExists(request.POST['value'])
                    return JsonResponse({'success': success, 'message': message})
                elif(request.POST['target']=='email'):
                    success, message = userfunctions.checkEmailExists(request.POST['value'], request.POST['curusername'])
                    return JsonResponse({'success': success, 'message': message})
                elif(request.POST['target']=='password'):
                    success, message = userfunctions.checkPasswordComplexity(request.POST['value'])
                    return JsonResponse({'success': success, 'message': message})
                return JsonResponse({'success': False, 'message': 'Could not verify login'})
            else:
                return JsonResponse({'success': False, 'message': 'Could not verify login'})
        elif (request.POST['action'] == 'changeemail') and ('username' in request.POST) and ('password' in request.POST) and ('email' in request.POST) and \
                    ('firstname' in request.POST) and ('lastname' in request.POST):
            if (userfunctions.validateNewUser(request.POST['username'], request.POST['password'], request.POST['email'], request.POST['firstname'], request.POST['lastname'])):
                try:
                    user = userfunctions.createUser(request.POST['username'], request.POST['password'], request.POST['email'], request.POST['firstname'], request.POST['lastname'])
                    if user is not None:
                        return redirect('/usermanagement')
                except Exception as exc:
                    logger.error('!views.createuser!: Could not create user. \n' + str(exc))
        elif (request.POST['action'] == 'changeemail') and ('email' in request.POST):
            try:
                success, message = userfunctions.checkEmailExists(request.POST['email'], request.POST['curusername'])
                if success:
                    if 'id' in request.POST:
                        success = userfunctions.changeEmail( request.POST['email'], request.POST['id'])
                    else:
                        success = userfunctions.changeEmail(request.POST['email'], request.user.id)
                    if user is not None:
                        return redirect('/changeuser')
            except Exception as exc:
                logger.error('!views.createuser!: Could not create user. \n' + str(exc))
    
    data['username']=request.user.username
    data['email']=request.user.email
    data['firstname']=request.user.first_name
    data['lastname']=request.user.last_name
            
    data['PAGE_TITLE'] = 'change user: CMS Infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'user/changeuser.html', data, content_type='text/html')






def clientview(request, clientid):
    valid, response = initRequestLogin(request)
    if not valid:
        return response
    data = modelgetters.form_client_data(clientid)
    if data is None:
        return redirect('/')            
    data['PAGE_TITLE'] = 'Client "'+ data['clientname'] +'": CMS Infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'views/client.html', data, content_type='text/html')


def allclientsview(request):
    valid, response = initRequestLogin(request)
    if not valid:
        return response
    data = {'allclients': modelgetters.form_all_clients_data()}
    if data is None:
        return redirect('/')            
    data['PAGE_TITLE'] = 'All clients: CMS Infotek'
    data['built'] = datetime.now().strftime("%H:%M:%S")
    return render(request, 'views/allclients.html', data, content_type='text/html')