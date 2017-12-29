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

# request urls and get the response, and be able to manipulate it, etc.
import urllib, urllib2

# json.loads() and json.dumps() loads and dumps a json string, taking it from
# valid json string to python dic object, and vice versa, respectively, with
# dumps() doing the appropriate escaping for us.
import json

# google oauth2 verification

from google.oauth2 import id_token
from google.auth.transport import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()



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

def signIn(request):
    token = request.POST['idtoken']
    CLIENT_ID = "1018666741394-fkb3lat9j0oceaor95lbcshittfrorp4.apps.googleusercontent.com"
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        pass
    return HttpResponse("umar alee")  

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
    all_sources_list = []
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
        if not keylist:
            allKeyList = []
            all_sources_list = Source.query()
            for source in all_sources_list:
                temp = []
                temp.append(source.key.id)
                temp.append(source.title)
                temp.append(source.description)
                allKeyList.append(temp)
            all_sources_list = allKeyList
    else:
        q = ''
        allKeyList = []
        all_sources_list = Source.query()
        for source in all_sources_list:
            temp = []
            temp.append(source.key.id)
            temp.append(source.title)
            temp.append(source.description)
            allKeyList.append(temp)
        all_sources_list = allKeyList
    #for source in sources:
    #    requested_issues_list.append(str(source.key))
    return render(request, "sourcebasesite/source.html", {'source_list': keylist, 'all_sources_list': all_sources_list, 'q': q})

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





