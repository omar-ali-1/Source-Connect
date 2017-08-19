from __future__ import unicode_literals

from django.db import models

from google.appengine.ext import ndb

from django.template.defaultfilters import slugify

from sourcebasesite.views import *


# find and implement efficient way to implement relationships between entities


class Issue(ndb.Model):
    """Profile -- User profile object"""
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    content = ndb.TextProperty()
    slug = ndb.ComputedProperty(lambda self: slugify(self.title))


class Argument(ndb.Model):
    """Profile -- User profile object"""
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    content = ndb.TextProperty()

# Relations
#----------
class IssueArgumentRel(ndb.Model):
    source = ndb.KeyProperty(kind=Issue,
                                   required=True)
    tag = ndb.KeyProperty(kind=Argument,
                                   required=True)
    relation = ndb.TextProperty(required=True)

class ArgumentSourceRel(ndb.Model):
    source = ndb.KeyProperty(kind=Argument,
                                   required=True)
    tag = ndb.KeyProperty(kind=Source,
                                   required=True)
    relation = ndb.TextProperty(required=True)

class IssueTagRel(ndb.Model):
    source = ndb.KeyProperty(kind=Issue,
                                   required=True)
    tag = ndb.KeyProperty(kind=Tag,
                                   required=True)
    relation = ndb.TextProperty()

class ArgumentTagRel(ndb.Model):
    source = ndb.KeyProperty(kind=Argument,
                                   required=True)
    tag = ndb.KeyProperty(kind=Tag,
                                   required=True)
    relation = ndb.TextProperty()

