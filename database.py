import sys

class Database(object):
    def __init__(self, name):
        self.name = name
        self.sources = [] # list of source objects
        self.tags = [] # list of Tag objects

    def addTag(self, tag):
        self.tags.append(tag)

    def deleteTag(self, tag):
        for i in xrange(len(self.tags)):
            if tag == self.tags[i]:
                self.tags.pop(i)
            else:
                for j in xrange(len(self.tags[i].relatedTags)):
                    if tag == self.tags[i].relatedTags[j]:
                        self.tags[i].relatedTags.pop(j)
                for j in xrange(len(self.tags[i].superTags)):
                    if tag == self.tags[i].superTags[j]:
                        self.tags[i].superTags.pop(j)
                for j in xrange(len(self.tags[i].subTags)):
                    if tag == self.tags[i].subTags[j]:
                        self.tags[i].subTags.pop(j)

    def addSource(self, source):
        self.sources.append(source)

    def deleteSource(self, source):
        for i in xrange(len(self.sources)):
            if source == self.sources[i]:
                self.sources.pop(i)