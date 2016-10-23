
class Tag(object):

    def __init__(self, name, sources=None, relatedTags=None):
        self.name = name
        self.sources = sources or [] # list of source object pointers
        self.relatedTags = relatedTags or []
        self.superTags = []
        self.subTags = []

    def addSource(self, source):
        self.sources.append(source)

    def getSources(self):
        return self.sources

    def deleteSource(self, sourceName):
        for i in xrange(len(self.sources)):
            if sourceName == self.sources[i].title:
                self.sources.pop(i)

    def addRelatedTag(self, tag):
        self.relatedTags.append(tag)

    def getRelatedTags(self):
        return self.relatedTags

    def deleteRelatedTag(self, tagName):
        for i in xrange(len(self.relatedTags)):
            if tagName == self.relatedTags[i].name:
                self.relatedTags.pop(i)

    def addSuperTag(self, tag):
        self.superTags.append(tag)


    def addSubTag(self, tag):
        self.subTags.append(tag)
