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
    all_issues_list = []
    issues = []
    if 'q' in request.GET:
        tags = Tag.query(Tag.title==request.GET['q'])
        q = request.GET['q']
        for tag in tags:
            for relation in IssueTagRel.query(IssueTagRel.tag==tag.key):
                issues.append(relation.issue.get())
        for issue in issues:
            temp = []
            temp.append(issue.key.id)
            temp.append(issue.title)
            temp.append(issue.description)
            keylist.append(temp)
        if not keylist:
            allKeyList = []
            all_issues_list = Issue.query()
            for issue in all_issues_list:
                temp = []
                temp.append(issue.key.id)
                temp.append(issue.title)
                temp.append(issue.description)
                allKeyList.append(temp)
            all_issues_list = allKeyList
    else:
        q = ''
        allKeyList = []
        all_issues_list = Issue.query()
        for issue in all_issues_list:
            temp = []
            temp.append(issue.key.id)
            temp.append(issue.title)
            temp.append(issue.description)
            allKeyList.append(temp)
        all_issues_list = allKeyList
    #for source in sources:
    #    requested_issues_list.append(str(source.key))
    return render(request, "issuesite/issue.html", {'issue_list': keylist, 'all_issues_list': all_issues_list, 'q': q})

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
    return render(request, "issuesite/claim_detail.html", {'claim': claim,'issue': issue, 'tags': tags, 'error':error})


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
        IssueClaimRel(issue = issue.key, claim = claim.key).put()
        error = "A claim with the title you entered already exists. Please edit this claim instead."
        return claimDetail(request, claimSlug, issueSlug, error)

def editClaim(request, issueID, claimID):
    claim = ndb.Key('Claim', claimID).get()
    issue = ndb.Key('Issue', issueID).get()
    tags = []
    for relation in ClaimTagRel.query(ClaimTagRel.claim==claim.key):
        tags.append(relation.tag.get().title.encode('utf-8'))
    return render(request, "issuesite/edit_claim.html", {'issue': issue, 'claim': claim, 'tags': tags})

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