import sys

class Database(object):
    def __init__(self, directory):
        self.directory = directory
        self.sources = [] # list of source objects
        self.tags = [] # list of Tag objects

    def addTag(self, tag):
        self.tags.append(tag)

    def deleteTag(self, tag):
        for i in xrange(len(self.tags)):
            if tag == self.tags[i]:
                self.tags.pop(i)

    def addSource(self, source):
        self.sources.append(source)

    def deleteSource(self, source):
        for i in xrange(len(self.sources)):
            if source == self.sources[i]:
                self.sources.pop(i)