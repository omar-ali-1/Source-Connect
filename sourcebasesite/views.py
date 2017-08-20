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

def detail(request, sourceID, error=None):
    sourceKey = ndb.Key(Source, sourceID)
    source = sourceKey.get()
    tags = []
    for relation in SourceTagRel.query(SourceTagRel.source==source.key):
                tags.append(relation.tag.get())
    return render(request, "sourcebasesite/source_detail.html", {'source': source, 'tags': tags, 'error':error})


def test(request):
    return render(request, "sourcebasesite/test.html")

def editSource(request, sourceID):
    key = ndb.Key('Source', sourceID)
    source = key.get()
    tags = []
    for relation in SourceTagRel.query(SourceTagRel.source==source.key):
                tags.append(relation.tag.get().title.encode('utf-8'))
    return render(request, "sourcebasesite/edit_source.html", {'source': source, 'tags': tags})

def newSource(request):
    post = request.POST
    slug = slugify(post['title'])
    source = Source.get_by_id(slug)
    if source is None:
        source = Source(title=post['title'])
        key = ndb.Key('Source', slug)
        source.key = key
        source.put()
        return HttpResponseRedirect(reverse('sourcebasesite:detail', args=(source.key.id(),)))
    else:
        error = "A source with the title you entered already exists. Please edit this source instead."
        return detail(request, slug, error)

def saveSource(request, sourceID):
    key = ndb.Key('Source', sourceID)
    source = key.get()
    tagNames = request.POST.getlist('taggles[]')
    tagNamesSet = set()
    for tagName in tagNames:
        tagNamesSet.add(tagName)

    #logging.info(tagNames)
    #logging.info(tagNamesSet)

    newTagNames = []
    oldTagNames = []
    needDelTags = []
    relations = SourceTagRel.query(SourceTagRel.source==source.key)

    #logging.info(relations)

    for relation in relations:
        oldTagNames.append(relation.tag.get().title)

    #logging.info(oldTagNames)

    oldTagNamesSet = set(oldTagNames)
    for tagName in tagNames:
        if tagName not in oldTagNamesSet:
            newTagNames.append(tagName)
    #logging.info("New tag names:")
    #logging.info(newTagNames)
    for tagName in oldTagNames:
        if tagName not in tagNamesSet:
            needDelTags.append(tagName)
    for tagName in newTagNames:
        tag = Tag.query(Tag.title == tagName).get()
        if tag is None:
            tag = Tag(title = tagName)
            tag.put()
        logging.info(tag.title)
        logging.info(tag.key)
        SourceTagRel(source = key, tag = tag.key).put()
    for tagName in needDelTags:
        SourceTagRel.query(SourceTagRel.tag==Tag.query(Tag.title == tagName).get().key).get().key.delete()
    post = request.POST
    source.description = post['description']
    title = post['title']
    tags = []
    if title != source.title:
        tags = SourceTagRel.query(SourceTagRel.source==source.key)
    source.title = title
    source.key.delete()
    source.key = ndb.Key(Source, source.slug)
    source.put()
    for tag in tags:
        tag.source = source.key
        tag.put()

    return HttpResponseRedirect(reverse('sourcebasesite:detail', args=(source.key.id(),)))

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





