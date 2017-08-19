from django.shortcuts import render
# from hotelsite.models import Review
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
# import mongoengine
# AppEngine Imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# Our App imports
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import ndb
from models import *
from google.appengine.ext.webapp.util import run_wsgi_app

from django.template.defaultfilters import slugify
from ast import literal_eval
import logging

# Create your views here.

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
    # add more here
}

def issue(request):
    #newsource = Source(title="some New Test Source", description='this is description')
    #newsource.put()
    #newsource.key = ndb.Key(Source, newsource.slug)
    #newsource.slug = slugify(newsource.title)
    #key = newsource.put()
    #newtag = Tag(title="new tag")
    #newtag.put()
    #tagkey = ndb.Key('Tag', 5785905063264256)
    #sourcekey = ndb.Key('Source', 'cups-and-milk')
    #relation = SourceTagRel(source=sourcekey, tag=tagkey).put()
    keylist = []
    sources = []
    if 'q' in request.GET:
        tags = Tag.query(Tag.title==request.GET['q'])
        q = request.GET['q']
        for tag in tags:
            for relation in SourceTagRel.query(SourceTagRel.tag==tag.key):
                sources.append(relation.source.get())
        for source in sources:
            temp = []
            temp.append(source.key.id)
            temp.append(source.title)
            temp.append(source.description)
            keylist.append(temp)
    else: 
        q = ""
    #for source in sources:
    #    keylist.append(str(source.key))
    return render(request, "sourcebasesite/source.html", {'source_dic': keylist, 'q': q})

def detail(request, sourceID, error=None):
    issueKey = ndb.Key(Issue, issueID)
    issue = issueKey.get()
    tags = []
    for relation in SourceTagRel.query(SourceTagRel.source==source.key):
                tags.append(relation.tag.get())
    return render(request, "sourcebasesite/source_detail.html", {'issue': issue, 'arguments': arguments, 'error':error})
