from __future__ import unicode_literals

from django.db import models

from google.appengine.ext import ndb

from django.template.defaultfilters import slugify

class Source(ndb.Model):
    """Profile -- User profile object"""
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    content = ndb.TextProperty()
    slug = ndb.ComputedProperty(lambda self: slugify(self.title))
    #id = ndb.ComputedProperty(lambda self: self.slug)

# Create your models here.
class Tag(ndb.Model):
    """Profile -- User profile object"""
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    slug = ndb.ComputedProperty(lambda self: slugify(self.title))

class SourceTagRel(ndb.Model):
    source = ndb.KeyProperty(kind=Source,
                                   required=True)
    tag = ndb.KeyProperty(kind=Tag,
                                   required=True)
    relation = ndb.TextProperty()