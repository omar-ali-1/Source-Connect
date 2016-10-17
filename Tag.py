
class Tag(object):
    def __init__(self, name, sources=None, relatedTags=None):
        self.name = name
        self.sources = sources or [] # list of Source object pointers
        self.relatedTags = relatedTags or []

    def getSources(self):
        return self.sources

    def getRelatedTags(self):
        return self.relatedTags
