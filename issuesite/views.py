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
from google.appengine.datastore.datastore_query import Cursor

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
'''
@ndb.tasklet
def get_search_issues_tasklet(tagTitle, cursor):
    ISSUES_PER_PAGE = 10
    relations_future = IssueTagRel.query(IssueTagRel.tag == tagTitle.key).fetch_async()
    cursor = Cursor(urlsafe=cursor)
    relations = relations_future.get_result()
    
    issues, next_cursor, more = Issue.query().fetch_page(
        ISSUES_PER_PAGE, start_cursor=cursor)
    tag = Tag.query(Tag.title==tagTitle)
'''
#-------------------------------
def _fetch_all_issues(request, cursor_url_safe=None, results_per_page=10):
    if cursor_url_safe:
        cursor = Cursor(urlsafe=cursor_url_safe)
        issue_list, next_cursor, there_is_next = Issue.query().order(Issue.title).fetch_page_async(
            results_per_page, start_cursor=cursor).get_result()
        issue_list_previous, previous_cursor, there_is_previous = Issue.query().order(-Issue.title).fetch_page_async(
            results_per_page, start_cursor=cursor).get_result()
        dummy, dummy_cursor, there_is_previous = Issue.query().order(-Issue.title).fetch_page(
            1, start_cursor=cursor)

        if there_is_previous:
            previous_cursor = previous_cursor.urlsafe()
        else:
            previous_cursor = ''
    else:
        issue_list, next_cursor, there_is_next = Issue.query().order(Issue.title).fetch_page_async(
            results_per_page).get_result()
        there_is_previous = False
        previous_cursor = ''
    enable_next = ''
    enable_previous = ''
    if not there_is_next:
        enable_next = 'disabled'
    if not there_is_previous:
        enable_previous = 'disabled'
    next_cursor = next_cursor.urlsafe()
    return render(request, "issuesite/issue.html", {'issue_list': issue_list, 
        'next_cursor': next_cursor, 'previous_cursor': previous_cursor, 'enable_previous': enable_previous, 'enable_next': enable_next})

def _fetch_tagged_issues(request, q, cursor_url_safe=None):
    tag_title_list = q.split()
    tag_key_list = [ndb.Key("Tag", slugify(tag_title)) for tag_title in tag_title_list]
    issue_tag_relation_list = IssueTagRel.query(IssueTagRel.tag.IN(tag_key_list)).fetch_async().get_result()
    issue_list = [relation.issue.get() for relation in issue_tag_relation_list]
    return render(request, "issuesite/issue.html", {'issue_list': issue_list, 'q': q})

issue_list = Issue.query().fetch_async().get_result()
def issue(request):
    get_dic = request.GET
    if ('q' in get_dic and len(get_dic['q']) == 0) or 'q' not in get_dic:
        if 'cursor' in get_dic:
            return _fetch_all_issues(request, cursor_url_safe=get_dic['cursor'])
        else:
            return _fetch_all_issues(request)

    else:
        q = get_dic['q']
        return _fetch_tagged_issues(request, q)

#-------------------------------

def issueDetail(request, issueID, error=None):
    issueKey = ndb.Key(Issue, issueID)
    issue = issueKey.get()
    tags = []
    claims = []
    for relation in IssueTagRel.query(IssueTagRel.issue==issueKey):
        tags.append(relation.tag.get())

    for relation in IssueClaimRel.query(IssueClaimRel.issue==issueKey):
        claims.append(relation.claim.get())

    return render(request, "issuesite/issue_detail.html", {'issue': issue, 'claims': claims, 'tags': tags, 'error':error})

def newIssue(request):
    post = request.POST
    slug = slugify(post['title'])
    issue = Issue.get_by_id(slug)
    if issue is None:
        issue = Issue(title=post['title'])
        key = ndb.Key('Issue', slug)
        issue.key = key
        issue.put()
        return HttpResponseRedirect(reverse('issuesite:issueDetail', args=(issue.key.string_id(),)))
    else:
        error = "A issue with the title you entered already exists. Please edit this issue instead."
        return issueDetail(request, slug, error)

# Editing Issue
# -------------
def getIssueKey(issueID):
    return ndb.Key('Issue', issueID)

def getTags(issueKey):
    '''Returns list of tag titles as strings'''
    tags = []
    for relation in IssueTagRel.query(IssueTagRel.issue==issueKey):
        tags.append(relation.tag.get().title.encode('utf-8'))
    return tags

def getClaims(issueKey):
    '''Returns list of claim objects'''
    claims = []
    claimQuery = IssueClaimRel.query(IssueClaimRel.issue==issueKey)
    for relation in claimQuery:
        claims.append(relation.claim.get())
    return claims

def getArguments(claims):
    argumentDic = dict()
    for claim in claims:
        argumentQuery = ClaimArgumentRel.query(ClaimArgumentRel.claim==claim.key)
        for relation in argumentQuery:
            if claim.title not in argumentDic:
                argumentDic[claim.title] = [[],[]]
            else:
                argument = relation.argument.get()
                if argument.function == "FOR":
                    argumentDic[claim.title][0].append(argument)
                else:
                    argumentDic[claim.title][1].append(argument)
    return argumentDic

def editIssue(request, issueID):
    issueKey = getIssueKey(issueID)
    issue = issueKey.get()
    tags = getTags(issueKey)
    claims = getClaims(issueKey)
    argumentDic = getArguments(claims)
    return render(request, "issuesite/edit_issue.html", {'issue': issue, 'tags': tags, 'claims': claims, 'arguments': argumentDic})


# -------------------------------------------------------------


def saveIssue(request, issueID):
    key = ndb.Key('Issue', issueID)
    logging.info("key:")
    logging.info(key)
    issue = key.get()
    title = request.POST['title']
    tagNames = request.POST.getlist('taggles[]')
    tagNamesSet = set()
    for tagName in tagNames:
        tagNamesSet.add(tagName)

    logging.info(tagNames)
    logging.info(tagNamesSet)

    newTagNames = []
    oldTagNames = []
    needDelTags = []
    relations = IssueTagRel.query(IssueTagRel.issue==issue.key)

    logging.info(relations)

    for relation in relations:
        oldTagNames.append(relation.tag.get().title)

    logging.info(oldTagNames)

    oldTagNamesSet = set(oldTagNames)
    for tagName in tagNames:
        if tagName not in oldTagNamesSet:
            newTagNames.append(tagName)
    logging.info("New tag names:")
    logging.info(newTagNames)
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
        IssueTagRel(issue = key, tag = tag.key).put()
    for tagName in needDelTags:
        IssueTagRel.query(IssueTagRel.tag==Tag.query(Tag.title == tagName).get().key).get().key.delete()
    post = request.POST
    issue.description = post['description']
    title = post['title']
    tags = []
    if title != issue.title:
        tags = IssueTagRel.query(IssueTagRel.issue==issue.key)
    issue.title = title
    issue.key.delete()
    issue.key = ndb.Key(Issue, issue.slug)
    issue.put()
    for tag in tags:
        tag.issue = issue.key
        tag.put()

    return HttpResponseRedirect(reverse('issuesite:issueDetail', args=(issue.key.id(),)))


# --------- Claims ----------------------------------------------------
'''
def claimDetail(request, claimID, error=None):
    claimKey = ndb.Key(Claim, claimID)
    claim = claimKey.get()
    tags = []
    for relation in ClaimTagRel.query(ClaimTagRel.claim==claim.key):
                tags.append(relation.tag.get())
    return render(request, "issuesite/claim_detail.html", {'claim': claim, 'tags': tags, 'error':error})
'''

def claimDetail(request, claimID, issueID, error=None):
    issue = ndb.Key(Issue, issueID).get()
    claim = ndb.Key(Claim, claimID).get()
    logging.info("claim:")
    logging.info(claim)
    tags = []
    for relation in ClaimTagRel.query(ClaimTagRel.claim==claim.key):
                tags.append(relation.tag.get())
    arguments_for_list = []
    arguments_against_list = []
    for relation in ClaimArgumentRel.query(ClaimArgumentRel.claim==claim.key):
        argument = relation.argument.get()
        if argument.function == "FOR":
            arguments_for_list.append(argument)
        elif argument.function == "AGAINST":
            arguments_against_list.append(argument)
        else:
            raise ValueError('Claim argument funciton was neither for nor against.')
    return render(request, "issuesite/claim_detail.html", {'claim': claim,'issue': issue, 'tags': tags,
        'arguments_for_list': arguments_for_list, 'arguments_against_list': arguments_against_list, 'error':error})


def newClaim(request, issueID):
    post = request.POST
    issueSlug = slugify(post['issueTitle'])
    claimSlug = slugify(post['claimTitle'])
    issue = Issue.get_by_id(issueSlug)
    claim = Claim.get_by_id(claimSlug)
    logging.info("claimID:")
    logging.info(claimSlug)
    if claim is None:
        claim = Claim(title=post['claimTitle'])
        key = ndb.Key('Claim', claimSlug)
        claim.key = key
        claim.put()
        IssueClaimRel(issue = issue.key, claim = claim.key).put()
        return HttpResponseRedirect(reverse('issuesite:claimDetail', kwargs={'claimID':claimSlug, 'issueID':issueSlug}))
    else:
        # wrong: if claim already exists, shouldn't creat relation : IssueClaimRel(issue = issue.key, claim = claim.key).put()
        error = "A claim with the title you entered already exists. Please edit this claim instead."
        return claimDetail(request, claimSlug, issueSlug, error)

def editClaim(request, issueID, claimID):
    claim = ndb.Key('Claim', claimID).get()
    issue = ndb.Key('Issue', issueID).get()
    tags = []
    for relation in ClaimTagRel.query(ClaimTagRel.claim==claim.key):
        tags.append(relation.tag.get().title.encode('utf-8'))
    arguments_for_list = []
    arguments_against_list = []
    for relation in ClaimArgumentRel.query(ClaimArgumentRel.claim==claim.key):
        argument = relation.argument.get()
        if argument.function == "FOR":
            arguments_for_list.append(argument)
        elif argument.function == "AGAINST":
            arguments_against_list.append(argument)
        else:
            raise ValueError('Claim argument funciton was neither for nor against.')
    return render(request, "issuesite/edit_claim.html", {'issue': issue, 'claim': claim, 'tags': tags, 
        'arguments_for_list': arguments_for_list, 'arguments_against_list': arguments_against_list,})

def saveClaim(request, issueID, claimID):
    key = ndb.Key('Claim', claimID)
    #logging.info("key:")
    #logging.info(key)
    claim = key.get()
    title = request.POST['title']
    tagNames = request.POST.getlist('taggles[]')
    tagNamesSet = set()
    for tagName in tagNames:
        tagNamesSet.add(tagName)

    #logging.info(tagNames)
    #logging.info(tagNamesSet)

    newTagNames = []
    oldTagNames = []
    needDelTags = []


    relations = ClaimTagRel.query(ClaimTagRel.claim==claim.key)

    logging.info(relations)

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
        #logging.info(tag.title)
        #logging.info(tag.key)
        ClaimTagRel(claim = key, tag = tag.key).put()
    for tagName in needDelTags:
        ClaimTagRel.query(ClaimTagRel.tag==Tag.query(Tag.title == tagName).get().key).get().key.delete()
    post = request.POST
    claim.description = post['description']
    title = post['title']
    tags = []
    if title != claim.title:
        tags = ClaimTagRel.query(ClaimTagRel.claim==claimKey)
    claim.title = title
    issueKey = ndb.Key('Issue', issueID)
    relation = IssueClaimRel.query(IssueClaimRel.issue==issueKey, IssueClaimRel.claim==claim.key).get()
    claim.key.delete()
    claim.key = ndb.Key('Claim', claim.slug)
    claim.put()
    relation.claim = claim.key
    relation.put()

    for tag in tags:
        tag.claim = claim.key
        tag.put()

    return HttpResponseRedirect(reverse('issuesite:claimDetail', args=(issueID, claim.key.id(),)))

# --------- Arguments ----------------------------------------------------

def argumentDetail(request, claimID, issueID, argumentID, error=None):
    issue = ndb.Key(Issue, issueID).get()
    claim = ndb.Key(Claim, claimID).get()
    argument = ndb.Key(Argument, argumentID).get()
    tags = []
    for relation in ClaimTagRel.query(ClaimTagRel.claim==claim.key):
                tags.append(relation.tag.get())

    arguments_for_list = []
    arguments_against_list = []
    for relation in ClaimArgumentRel.query(ClaimArgumentRel.claim==claim.key, ClaimArgumentRel.argument==argument.key):
        pass
    return render(request, "issuesite/argument_detail.html", {'claim': claim,'issue': issue, 'argument': argument, 'tags': tags, 'error':error})


def newArgument(request, claimID, issueID):
    post = request.POST
    issueSlug = slugify(post['issueTitle'])
    claimSlug = slugify(post['claimTitle'])
    argumentSlug = slugify(post['argumentTitle'])
    issue = Issue.get_by_id(issueSlug)
    claim = Claim.get_by_id(claimSlug)
    argument = Argument.get_by_id(argumentSlug)
    if argument is None:
        argument = Argument(title=post['argumentTitle'])
        key = ndb.Key('Argument', argumentSlug)
        argument.key = key
        argument.function = post['radio']
        argument.put()
        ClaimArgumentRel(claim = claim.key, argument = argument.key, relation = post['radio']).put()
        return HttpResponseRedirect(reverse('issuesite:argumentDetail', kwargs={'claimID':claimSlug, 'issueID':issueSlug, 'argumentID': argumentSlug}))
    else:
        # wrong: if claim already exists, shouldn't creat relation : IssueClaimRel(issue = issue.key, claim = claim.key).put()
        error = "A claim with the title you entered already exists. Please edit this claim instead."
        return argumentDetail(request, claimSlug, issueSlug, argumentSlug, error)

def editArgument(request, issueID, claimID, argumentID):
    claim = ndb.Key('Claim', claimID).get()
    issue = ndb.Key('Issue', issueID).get()
    argument = ndb.Key('Argument', argumentID).get()
    tags = []
    for relation in ArgumentTagRel.query(ArgumentTagRel.argument==argument.key):
        tags.append(relation.tag.get().title.encode('utf-8'))
    return render(request, "issuesite/edit_argument.html", {'issue': issue, 'claim': claim, 'argument': argument, 'tags': tags})

def saveArgument(request, issueID, claimID, argumentID):
    key = ndb.Key('Argument', argumentID)
    #logging.info("key:")
    #logging.info(key)
    argument = key.get()
    title = request.POST['title']
    tagNames = request.POST.getlist('taggles[]')
    tagNamesSet = set()
    for tagName in tagNames:
        tagNamesSet.add(tagName)

    #logging.info(tagNames)
    #logging.info(tagNamesSet)

    newTagNames = []
    oldTagNames = []
    needDelTags = []


    relations = ArgumentTagRel.query(ArgumentTagRel.argument==argument.key)

    logging.info(relations)

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
        #logging.info(tag.title)
        #logging.info(tag.key)
        ArgumentTagRel(argument = key, tag = tag.key).put()
    for tagName in needDelTags:
        ArgumentTagRel.query(ArgumentTagRel.tag==Tag.query(Tag.title == tagName).get().key).get().key.delete()
    post = request.POST
    argument.description = post['description']
    title = post['title']
    tags = []
    if title != argument.title:
        tags = ArgumentTagRel.query(ArgumentTagRel.argument==argument.key)
    argument.title = title
    claimKey = ndb.Key('Claim', claimID)
    relation = ClaimArgumentRel.query(ClaimArgumentRel.claim==claimKey, ClaimArgumentRel.argument==argument.key).get()
    argument.key.delete()
    argument.key = ndb.Key('Argument', slugify(argument.title))
    argument.put()
    relation.argument = argument.key
    relation.put()

    for tag in tags:
        tag.argument = argument.key
        tag.put()

    return HttpResponseRedirect(reverse('issuesite:argumentDetail', args=(issueID, claimID, argument.key.id(),)))