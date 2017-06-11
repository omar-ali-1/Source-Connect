"""sourcebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from sourcebasesite.views import *
#from django.views.generic import RedirectView

# TODO: redirect urls that don't match anything to home (/source/)

urlpatterns = [
    # url(r'^$', RedirectView.as_view(url='/source/')), # change to source/
    url(r'^$', home, name='home'),
    url(r'^about/', about, name='about'),
    url(r'^discuss/', discuss, name='discuss'),
    url(r'^read/', read, name='read'),
    url(r'^act/', act, name='act'),
    url(r'^about/', about, name='about'),
    url(r'^contact/', contact, name='contact'),
    url(r'^test/', test, name='test'),
    #url(r'^source/', source, name='source'),
    url(r'^source/', include('sourcebasesite.urls')),
    url(r'^admin/', admin.site.urls)
]