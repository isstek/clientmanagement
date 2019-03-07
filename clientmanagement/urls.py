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

from clientmanagement import views as clientmanagement_views
from clientmanagement import generatefileviews as generate_files
from models import views as models_views


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
    path('client', models_views.clientForm, name='newclient'),
    path('clients/', clientmanagement_views.allclientsview, name='changecomputer'),
    path('usermanagement', clientmanagement_views.usermanagement, name='usermanagement'),
    path('createuser', clientmanagement_views.createuser, name='createuser'),
    path('changeuser', clientmanagement_views.changeuser, name='changeuser'),
    path('', clientmanagement_views.homepage, name='homepage'),
    path('login', clientmanagement_views.loginpage, name='loginpage'),
    path('logout', clientmanagement_views.logout, name='logout'),
    path('admin/', admin.site.urls),
    re_path(r'^.*$', clientmanagement_views.homepage),
    path('testmodule/', include('clientmanagement.testmodule.urls')),
]
