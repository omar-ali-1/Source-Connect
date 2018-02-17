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
from issuesite.models import *



from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
    # add more here
}

def admin(request):
    return render(request, "sourcebasesite/admin.html")

def createEntities(request):
    import random, string
    def randomword(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    issue_count = 35
    claim_count = 3
    argument_count = 4
    for i in xrange(issue_count):
        title_length = random.randint(6, 14)
        title = string.join([randomword(random.randint(4,8)) for i in xrange(title_length)])
        desc_length = random.randint(600, 1000)
        description = string.join([randomword(random.randint(4,8)) for i in xrange(desc_length)])
        issue = Issue(title=title, description=description)
        key = ndb.Key('Issue', slugify(title))
        issue.key = key
        issue.put()
        for j in xrange(claim_count):
            title_length = random.randint(6, 14)
            title = string.join([randomword(random.randint(4,8)) for i in xrange(title_length)])
            desc_length = random.randint(600, 1000)
            description = string.join([randomword(random.randint(4,8)) for i in xrange(desc_length)])
            claim = Claim(title=title, description=description)
            key = ndb.Key('Claim', slugify(title))
            claim.key = key
            claim.put()
            IssueClaimRel(issue = issue.key, claim = claim.key).put()
            for k in xrange(argument_count):
                title_length = random.randint(6, 14)
                title = string.join([randomword(random.randint(4,8)) for i in xrange(title_length)])
                desc_length = random.randint(600, 900)
                description = string.join([randomword(random.randint(4,8)) for i in xrange(desc_length)])
                if k < argument_count/2:
                    func = 'FOR'
                else:
                    func = 'AGAINST'
                argument = Argument(title=title, description=description)
                key = ndb.Key('Argument', slugify(title))
                argument.key = key
                argument.put()
                ClaimArgumentRel(claim=claim.key, argument=argument.key, relation=func).put()
    return HttpResponse("Entities have been created. <a href='/issues/'>Issues</a>")

def deleteEntities(request)  :
    ndb.delete_multi(
    Issue.query().fetch(keys_only=True))
    ndb.delete_multi(
    Argument.query().fetch(keys_only=True))
    ndb.delete_multi(
    Claim.query().fetch(keys_only=True))
    ndb.delete_multi(
    IssueClaimRel.query().fetch(keys_only=True))
    ndb.delete_multi(
    ClaimArgumentRel.query().fetch(keys_only=True))
    return HttpResponse("Entities have been deleted. <a href='/issues/'>Issues</a>")

def home(request):
    return render(request, "sourcebasesite/home.html")



def userProfile(request):
    return render(request, "sourcebasesite/user_profile.html")

def fetchProfile(request):
    
    #print "i am here"
    # print request
    id_token = request.META['HTTP_AUTHORIZATION'].split(' ').pop()
    print id_token
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    profile = query_database(claims['sub'], claims)


    return HttpResponse(json.dumps(profile))

def query_database(user_id, claims):
    """Fetches all notes associated with user_id.

    Notes are ordered them by date created, with most recent note added
    first.
    """
    #ancestor_key = ndb.Key(Note, user_id)
    user = User.query(User.userID==user_id).fetch()

    if not user:
        bio = "Hello my name is whatever! Hello my name is whatever! Hello my name is whatever! \
        Hello my name is whatever! Hello my name is whatever! Hello my name is whatever! Hello my name is whatever!"
        try:
            claims['email']
            user = User(firstName = claims['name'], userID = claims['sub'], email = claims['email'], bio = bio)
        except:
            user = User(firstName = claims['name'], userID = claims['sub'], bio = bio)
        user.put()
    else:
        user = user[0]
    #notes = query.fetch()

    user_data = []
    user_data.append({
        'name': user.firstName,
        'bio': user.bio
        })
    '''
    for note in notes:
        note_messages.append({
            'friendly_id': note.friendly_id,
            'message': note.message,
            'created': note.created
        })
    '''
    return user_data





def signIn(request):
    # Verify Firebase auth.
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    else:
        return HttpResponse("Welcome, " + claims['sub'] + "!")

        '''
    token = request.POST['idtoken']
    CLIENT_ID = "1018666741394-1jtidvl576osjq6k10uijghd9qu7j38v.apps.googleusercontent.com"
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
    if "getBio" in request.POST:
        user = User.query(User.userID==userid).fetch()
        if user:
            bio = user.bio
            return HttpResponse(bio)
        else:
            user = User(firstName = idinfo['name'], userID = userid, email = idinfo['email'])
            user.put()
            bio = user.bio
            return HttpResponse(bio)
    else:
        return HttpResponse(userid)  
    '''
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





