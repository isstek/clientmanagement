"""visualanalyticsplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from clientmanagement import views as clientmanagement_views
from clientmanagement import loginform as clientmanagement_loginform
from clientmanagement import generatefileviews as generate_files
from models import views as models_views
from models.email import mailbox


urlpatterns = [
    path('clients/', clientmanagement_views.allclientsview, name='allclients'),
    path('computers/', clientmanagement_views.allcomputersview, name='allcomputers'),
    path('clients/<int:clientid>', clientmanagement_views.clientview, name='oneclient'),
    path('clients/<int:clientid>/computer', models_views.computerForm, name='clientcomputer'),
    path('clients/<int:clientid>/printer', models_views.printerForm, name='clientprinter'),
    path('clients/<int:clientid>/person', models_views.personForm, name='clientperson'),
    path('clients/<int:clientid>/domain', models_views.domainForm, name='clientdomain'),
    path('clients/<int:clientid>/router', models_views.routerForm, name='clientrouter'),
    path('clients/<int:clientid>/netequipment', models_views.otherNetEquipmentForm, name='clientothernetequip'),
    path('clients/<int:clientid>/joindomainfile', generate_files.downloadConnectDomainFile, name='clientjoindomainfile'),
    path('tickets/submit', models_views.submitTicketForm, name='ticket_submit'),
    path('tickets/submitted', clientmanagement_views.ticketdoneview, name='ticket_submitted'),
    path('tickets/<int:ticketid>/change', models_views.changeTicketForm, name='ticket_change'),
    path('tickets/<uuid:ticketuuid>', models_views.viewTicketDirectView, name='ticket_view_direct'),
    path('tickets/<uuid:ticketuuid>/addcomment', models_views.addCommentToTicketView, name='ticket_add_comment'),
    re_path(r'^tickets/(?P<reqtype>(a|c|o|))', clientmanagement_views.allticketsview, name='alltickets'),
    path('statistics/', clientmanagement_views.statisticsview, name='statistics'),
    path('client', models_views.clientForm, name='newclient'),
    path('updates/', clientmanagement_views.systemupdatesview, name='updates'),
    path('updates/post', models_views.PostSystemUpdate, name='postupdate'),
    path('usermanagement/', clientmanagement_views.usermanagement, name='usermanagement'),
    path('usermanagement/adduser', models_views.addUserForm, name='adduser'),
    path('', clientmanagement_views.homepage, name='homepage'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=clientmanagement_loginform.my_reset_password_form), {'password_reset_form':clientmanagement_loginform.my_reset_password_form, 'form_class': clientmanagement_loginform.my_reset_password_form}, 'password_reset'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=clientmanagement_loginform.MyAuthLoginForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^.*$', clientmanagement_views.homepage),
    path('testmodule/', include('clientmanagement.testmodule.urls')),
]


mailbox.initiateEmailCheck()