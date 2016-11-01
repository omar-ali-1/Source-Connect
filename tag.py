import TrieStructure

class Tag(object):

    def __init__(self, name):
        self.name = name
        self.deleted = False
        self.sources = TrieStructure.TrieTree() # Trie of source object pointers
        self.relatedTags = TrieStructure.TrieTree()
        self.superTags = TrieStructure.TrieTree()
        self.subTags = TrieStructure.TrieTree()

    def addSource(self, source):
        self.sources.insert(source.name, source)

    def getSources(self):
        return self.sources

    def deleteSource(self, sourceName):
            node = self.sources.head
            for letter in sourceName:
                if letter in node.children:
                    node = node.children[letter]
                else:
                    locationExists = False
                    break
            if locationExists:
                node.word = None
                node.item = None

    def addRelatedTag(self, tag):
        self.relatedTags.insert(tag.name, tag)

    def getRelatedTags(self):
        return self.relatedTags

    def deleteRelatedTag(self, tagName):
        node = self.relatedTags.head
        locationExists = True
        for letter in tagName:
            if letter in node.children:
                node = node.children[letter]
            else:
                locationExists = False
                break
        if locationExists:
            node.word = None
            node.item = None

    def addSuperTag(self, tag):
        self.superTags.insert(tag.name, tag)

    def getSuperTags(self):
        return self.superTags

    def deleteSuperTag(self, tagName):
        node = self.superTags.head
        locationExists = True
        for letter in tagName:
            if letter in node.children:
                node = node.children[letter]
            else:
                locationExists = False
                break
        if locationExists:
            node.word = None
            node.item = None

    def addSubTag(self, tag):
        self.subTags.insert(tag.name, tag)

    def getSubTags(self):
        return self.subTags

    def deleteSubTag(self, tagName):
        node = self.subTags.head
        locationExists = True
        for letter in tagName:
            if letter in node.children:
                node = node.children[letter]
            else:
                locationExists = False
                break
        if locationExists:
            node.word = None
            node.item = None