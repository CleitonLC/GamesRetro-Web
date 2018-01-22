"""GamesRetro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from modules.core import views as view_core
from django.conf import settings
from modules.core.api import ConfigurationsController
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', view_core.index),
    url(r'^admin/', admin.site.urls),
    #url(r'^api/core/', include('modules.core.urls')),
    url(r'^home', view_core.index),
    url(r'^roms/list_roms/', view_core.view_roms),
    url(r'^roms/load_roms$', ConfigurationsController().load_games),
    url(r'^roms/open_roms/$', ConfigurationsController().open_games),
    url(r'^roms/open_nesbox/$', ConfigurationsController().open_nesbox),

]