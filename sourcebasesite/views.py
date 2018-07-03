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


def verifyOrCreateUser(request):
    id_token = request.META['HTTP_AUTHORIZATION'].split(' ').pop()
    print id_token
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401

    user = User.query(User.userID==claims['sub']).fetch()
    print claims
    if user:
        return HttpResponse(json.dumps({'status':'success'}))
    else:
        bio = "Your bio goes here."
        try:
            claims['email']
            #TODO: fix first last name issue here
            user = User(firstName = claims['name'], userID = claims['sub'], email = claims['email'], bio = bio)
        except:
            user = User(firstName = claims['name'], userID = claims['sub'], bio = bio)
        if 'picture' in claims:
            user.picture = claims['picture']
        user.put()
    return HttpResponse(json.dumps({'status':'success'}))

def userProfile(request, userID):
    user = _getUserObject(userID)
    error = None
    if not user:
        error = "Sorry, this user does not exist!"
    return render(request, "sourcebasesite/user_profile.html", {'user': user, 'error':error})

def _getUserObject(userID):
    user = User.query(User.userID==userID).fetch()
    if user:
        return user[0]
    else:
        return None


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
    
    if user:
        user = user[0]
    else:
        bio = "Hello my name is whatever! Hello my name is whatever! Hello my name is whatever! \
        Hello my name is whatever! Hello my name is whatever! Hello my name is whatever! Hello my name is whatever!"
        try:
            claims['email']
            user = User(firstName = claims['name'], userID = claims['sub'], email = claims['email'], bio = bio)
        except:
            user = User(firstName = claims['name'], userID = claims['sub'], bio = bio)
        user.put()

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



def _fetch_all_sources(request, cursor_url_safe=None, results_per_page=7):
    if cursor_url_safe:
        cursor = Cursor(urlsafe=cursor_url_safe)
        source_list, next_cursor, there_is_next = Source.query().order(Source.title).fetch_page_async(
            results_per_page, start_cursor=cursor).get_result()
        source_list_previous, previous_cursor, there_is_previous = Source.query().order(-Source.title).fetch_page_async(
            results_per_page, start_cursor=cursor).get_result()
        dummy, dummy_cursor, there_is_previous = Source.query().order(-Source.title).fetch_page(
            1, start_cursor=cursor)

        if there_is_previous:
            previous_cursor = previous_cursor.urlsafe()
        else:
            previous_cursor = ''
    else:
        source_list, next_cursor, there_is_next =Source.query().order(Source.title).fetch_page_async(
            results_per_page).get_result()
        there_is_previous = False
        previous_cursor = ''
    enable_next = ''
    enable_previous = ''
    if not there_is_next:
        enable_next = 'disabled'
    if not there_is_previous:
        enable_previous = 'disabled'
    if next_cursor:
        next_cursor = next_cursor.urlsafe()
    return render(request, "sourcebasesite/sources.html", {'source_list': source_list, 
        'next_cursor': next_cursor, 'previous_cursor': previous_cursor, 'enable_previous': enable_previous, 'enable_next': enable_next})

def _fetch_tagged_sources(request, q, cursor_url_safe=None):
    tag_title_list = q.split()
    tag_key_list = [ndb.Key("Tag", slugify(tag_title)) for tag_title in tag_title_list]
    source_tag_relation_list = SourceTagRel.query(SourceTagRel.tag.IN(tag_key_list)).fetch_async().get_result()
    source_list = [relation.source.get() for relation in source_tag_relation_list]
    return render(request, "sourcebasesite/sources.html", {'source_list': source_list, 'q': q})

source_list = Source.query().fetch_async().get_result()
def source(request):
    # _delete_data()
    # _create_data()
    get_dic = request.GET
    if ('q' in get_dic and len(get_dic['q']) == 0) or 'q' not in get_dic:
        if 'cursor' in get_dic:
            return _fetch_all_sources(request, cursor_url_safe=get_dic['cursor'])
        else:
            return _fetch_all_sources(request)

    else:
        q = get_dic['q']
        return _fetch_tagged_sources(request, q)


def sourceDetail(request, sourceID, error=None):
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

'''
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
        return detail(request, slug, error)'''

def newSource(request):
    try:
        # logging.info("======== We are here in newIssue================")
        id_token = request.META['HTTP_AUTHORIZATION'].split(' ').pop()
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, HTTP_REQUEST)
        if not claims:
            return 'Unauthorized', 401
        # logging.info(claims)
        # user = User.query(User.userID==claims['sub']).fetch()

        post = request.POST
        slug = slugify(post['title'])
        source = Source.get_by_id(slug)
        if source is None:
            source = Source(title=post['title'], description=post['description'], author=[claims['name'], claims['email'], claims['sub']])
            source.key = ndb.Key('Source', slug)
            source.put()
            return HttpResponse(json.dumps({'status':'success', 'link': slug}))
        else:
            return HttpResponse(json.dumps({'status':'exists', 'link': slug}))
    except Exception as e:
        logging.info(e)

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

    return HttpResponseRedirect(reverse('sourcebasesite:sourceDetail', args=(source.key.id(),)))

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





