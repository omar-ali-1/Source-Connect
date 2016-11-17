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
        source.tags.insert(self.name, self)

    def deleteTaggedSource(self, sourceName):
        taggedSource = self.sources.search(sourceName, 0)[0][0]
        self.sources.deleteItem(sourceName)
        taggedSource.tags.deleteItem(self.name)

    def getSources(self):
        return self.sources

    '''def deleteSource(self, sourceName):
            node = self.sources.head
            for letter in sourceName:
                if letter in node.children:
                    node = node.children[letter]
                else:
                    locationExists = False
                    break
            if locationExists:
                node.word = None
                node.item = None'''

    def addRelatedTag(self, tag):
        self.relatedTags.insert(tag.name, tag)
        tag.relatedTags.insert(self.name, self)

    def getRelatedTags(self):
        return self.relatedTags

    def deleteRelatedTag(self, tagName):
        relatedTag = self.relatedTags.search(tagName, 0)[0][0]
        self.relatedTags.deleteItem(tagName)
        relatedTag.relatedTags.deleteItem(self.name)

    def addSuperTag(self, tag):
        self.superTags.insert(tag.name, tag)
        tag.subTags.insert(self.name, self)

    def getSuperTags(self):
        return self.superTags

    def deleteSuperTag(self, tagName):
        superTag = self.superTags.search(tagName, 0)[0][0]
        self.superTags.deleteItem(tagName)
        superTag.subTags.deleteItem(self.name)

    def addSubTag(self, tag):
        self.subTags.insert(tag.name, tag)
        tag.superTags.insert(self.name, self)

    def getSubTags(self):
        return self.subTags

    def deleteSubTag(self, tagName):
        subTag = self.subTags.search(tagName, 0)[0][0]
        self.subTags.deleteItem(tagName)
        subTag.superTags.deleteItem(self.name)