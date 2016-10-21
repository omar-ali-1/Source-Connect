
class Tag(object):

    def __init__(self, name, sources=None, relatedTags=None):
        self.name = name
        self.sources = sources or [] # list of source object pointers
        self.relatedTags = relatedTags or []

    def addSource(self, source):
        self.sources.append(source)

    def deleteSource(self, source):
        for i in xrange(len(self.sources)):
            if source == self.sources[i]:
                self.sources.pop(i)

    def getSources(self):
        return self.sources

    def getRelatedTags(self):
        return self.relatedTags
