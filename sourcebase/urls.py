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
# TODO: for new source, or issue, or anything, new should not come after the thing in url. eg /source/new/, because 
# for some reason the matcher does not match to newThing view, but rather to detail view with "new" as the id of requested
# thing. When action="{% url 'issuesite:newIssue' %}" is used, the url looks the same, but routs properly for some reason.
# look into it and see, but change to something like /new/source/ anyway.
urlpatterns = [
    # url(r'^$', RedirectView.as_view(url='/source/')), # change to source/
    url(r'^$', source, name='source'),
    url(r'^about/', about, name='about'),
    url(r'^discuss/', discuss, name='discuss'),
    url(r'^read/', read, name='read'),
    url(r'^act/', act, name='act'),
    url(r'^about/', about, name='about'),
    url(r'^contact/', contact, name='contact'),
    url(r'^test/', test, name='test'),
    url(r'^source/', include('sourcebasesite.urls', namespace='sourcebasesite')),
    #url(r'^source/', source, name='source'),
    url(r'^issues/', include('issuesite.urls', namespace='issuesite')),
    url(r'^admin/', admin, name='admin'),
    url(r'^tokensignin/', signIn, name='signIn'),
    url(r'^createEntities/', createEntities, name='createEntities'),
    url(r'^deleteEntities/', deleteEntities, name='deleteEntities'),
    url(r'^me/', userProfile, name='userProfile'),
    url(r'^fetchProfile/', fetchProfile, name='fetchProfile'),
    url(r'^users/(?P<userID>[a-zA-Z0-9-_]+)/$', userProfile, name='userProfile'),
    url(r'^verifyOrCreateUser/$', verifyOrCreateUser, name='verifyOrCreateUser')
]
