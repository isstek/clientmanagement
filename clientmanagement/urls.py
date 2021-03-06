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
from django.urls import path, include, re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse

from clientmanagement import views as clientmanagement_views
from clientmanagement import loginform as clientmanagement_loginform
from clientmanagement import generatefileviews as generate_files
from models import views as models_views
from models.email import mailbox


urlpatterns = [
    path('clients/', clientmanagement_views.allclientsview, name='allclients'),
    path('computers/', clientmanagement_views.allcomputersview, name='allcomputers'),
    path('people/', clientmanagement_views.allpeopleview, name='allpeople'),

    path('clients/<int:clientid>', clientmanagement_views.clientview, name='oneclient'),
    path('clients/<int:clientid>/printer', models_views.printerForm, name='clientprinter'),
    path('clients/<int:clientid>/computer', models_views.computerForm, name='clientcomputer'),
    path('clients/<int:clientid>/person', models_views.personForm, name='clientperson'),
    path('clients/<int:clientid>/domain', models_views.domainForm, name='clientdomain'),
    path('clients/<int:clientid>/router', models_views.routerForm, name='clientrouter'),
    path('clients/<int:clientid>/netequipment', models_views.otherNetEquipmentForm, name='clientothernetequip'),
    path('clients/<int:clientid>/joindomainfile', generate_files.downloadConnectDomainFile, name='clientjoindomainfile'),
    path('clients/<int:clientid>/addcomputersoftware', generate_files.downloadAddComputerSoftware, name='clientaddcomputersoftware'),
    path('clients/<int:clientid>/addcomputerconfig', generate_files.downloadAddComputerConfigFile, name='clientaddcomputerconfig'),

    path('tickets/submit', models_views.submitTicketForm, name='ticket_submit'),
    path('tickets/submitted', clientmanagement_views.ticketdoneview, name='ticket_submitted'),
    path('tickets/<int:ticketid>/change', models_views.changeTicketForm, name='ticket_change'),
    path('tickets/<uuid:ticketuuid>', models_views.viewTicketDirectView, name='ticket_view_direct'),
    re_path(r'^tickets/(?P<ticketuuid>\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)/files/(?P<filename>[a-zA-Z0-9\.\(\)_\-+=!@#%]+)', models_views.downloadFileFromTicket, name='get_ticket_file'),
    re_path(r'^tickets/(?P<ticketuuid>\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)/v/files/(?P<filename>[a-zA-Z0-9\.\(\)_\-+=!@#%]+)', models_views.viewFileFromTicket, name='get_ticket_file_view'),
    re_path(r'^tickets/(?P<ticketuuid>\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)/(?P<commentid>\d+)/files/(?P<filename>[a-zA-Z0-9\.\(\)_\-+=!@#%]+)', models_views.downloadFileFromComment, name='get_comment_file'),
    re_path(r'^tickets/(?P<ticketuuid>\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)/(?P<commentid>\d+)/v/files/(?P<filename>[a-zA-Z0-9\.\(\)_\-+=!@#%]+)', models_views.viewFileFromComment, name='get_comment_file_view'),
    path('tickets/<uuid:ticketuuid>/addcomment', models_views.addCommentToTicketView, name='ticket_add_comment'),
    re_path(r'^tickets/(?P<reqtype>(a|c|o|))', clientmanagement_views.allticketsview, name='alltickets'),

    path('note', models_views.AddSecretNoteView, name='new_note'),
    path('notes/', models_views.allSecretNotesView, name='all_notes'),
    re_path(r'^notes/(?P<reqtype>(|a|u))$', models_views.allSecretNotesView, name='all_notes'),
    path('notes/<int:noteid>', models_views.SecretNoteInternalView, name='note_internal'),
    path('notes/<int:noteid>/change', models_views.changeTicketForm, name='note_change'),
    path('notes/c/<uuid:noteuuid>', models_views.viewSecretNoteViewClose, name='note_close'),
    path('notes/o/<uuid:noteuuid>', models_views.viewSecretNoteViewOpen, name='note_open'),

    re_path(r'^tool/(?P<tool_type>(l|f))$', models_views.AddNewToolView, name='new_tool'),
    re_path(r'^tools/(?P<tool_type>(l|f|))$', clientmanagement_views.allToolsView, name='all_tools'),
    path('tool/f/d/<uuid:tooluuid>', models_views.downloadToolPublic, name='download_tool_public'),
    path('tool/f/d/p/<uuid:tooluuid>', models_views.downloadTool, name='download_tool'),

    path('statistics/', clientmanagement_views.statisticsview, name='statistics'),
    path('client', models_views.clientForm, name='newclient'),
    path('client/<int:clientid>/r', models_views.downloadRouterSettings, name='download_router_settings'),

    path('wiki/', clientmanagement_views.allWikiArticlesView, name='all_wiki'),
    path('wiki/new', models_views.createWikiArticle, name='wiki_new'),
    path('wiki/<uuid:wikiuuid>', clientmanagement_views.wikiArticleView, name='wiki_art'),

    path('updates/', clientmanagement_views.systemupdatesview, name='updates'),
    path('updates/post', models_views.PostSystemUpdate, name='postupdate'),

    path('usermanagement/', clientmanagement_views.usermanagement, name='usermanagement'),
    path('usermanagement/adduser', models_views.addUserForm, name='adduser'),
    path('', clientmanagement_views.homepage, name='homepage'),

    path('me', clientmanagement_views.userpersonalpage, name='personal_page'),
    path('me/<int:deleted>/<int:deletedpage>', clientmanagement_views.userpersonalpage, name='personal_page_uri'),
    path('me/delete_api', clientmanagement_views.deletepersonalapikey, name='delete_my_api_key'),
    path('me/cms_interactive', generate_files.downloadUserCMSInteractionSoftware, name='cms_interactive_software'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=clientmanagement_loginform.my_reset_password_form, 
    html_email_template_name='registration/forgot_password.htm'), 
    {'password_reset_form':clientmanagement_loginform.my_reset_password_form, 
    'form_class': clientmanagement_loginform.my_reset_password_form}, 'password_reset'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=clientmanagement_loginform.MyAuthLoginForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include('api_app.urls')),
    re_path(r'^.*$', clientmanagement_views.homepage),
    path('testmodule/', include('clientmanagement.testmodule.urls')),
]


mailbox.initiateEmailCheck()