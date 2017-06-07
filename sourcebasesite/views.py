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

# Create your views here.

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
    # add more here
}

def home(request):
    return render(request, "sourcebasesite/home.html")

def source(request):
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

def detail(request, sourceID):
    sourceKey = ndb.Key(Source, sourceID)
    source = sourceKey.get()
    tags = []
    for relation in SourceTagRel.query(SourceTagRel.source==source.key):
                tags.append(relation.tag.get())
    return render(request, "sourcebasesite/source_detail.html", {'source': source, 'tags': tags})


def test(request):
    return render(request, "sourcebasesite/test.html")

def editSource(request, sourceID):
    key = ndb.Key('Source', sourceID)
    source = key.get()
    tags = []
    for relation in SourceTagRel.query(SourceTagRel.source==source.key):
                tags.append(relation.tag.get())
    return render(request, "sourcebasesite/edit_source.html", {'source': source, 'tags': tags})

def newSource(request):
    post = request.POST
    source = Source(title=post['title'])
    key = ndb.Key('Source', slugify(post['title']))
    source.key = key
    source.put()
    return HttpResponseRedirect(reverse('detail', args=(source.key.id(),)))

def saveSource(request, sourceID):
    key = ndb.Key('Source', sourceID)
    source = key.get()
    title = request.POST['title']
    description = request.POST['description']
    source.title = title
    source.description = description
    source.key.delete()
    source.key = ndb.Key(Source, source.slug)
    source.put()
    return HttpResponseRedirect(reverse('detail', args=(source.key.id(),)))

def discuss(request):
    return render(request, "sourcebasesite/discuss.html")

def read(request):
    return render(request, "sourcebasesite/read.html")

def contact(request):
    return render(request, "sourcebasesite/contact.html")

def act(request):
    return render(request, "sourcebasesite/act.html")

def about(request):
    return render(request, "sourcebasesite/about.html")





