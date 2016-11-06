import sys, tag, TrieStructure, shutil

class Database(object):
    def __init__(self, name):
        self.name = name
        self.sources = TrieStructure.TrieTree() # Trie Tree of source objects
        self.tags = TrieStructure.TrieTree() # Trie Tree of Tag objects

    def addTag(self, tag): # arg is Tag object
        self.tags.insert(tag.name, tag)

    def searchTags(self, tagName, maxCost=0): # arg should be Tag.name
        return self.tags.search(tagName, maxCost) #list of found Tag objects

    def addSource(self, source):
        self.sources.insert(source.name, source)

    def searchSources(self, sourceName, maxCost=0): # arg is Source object
        return self.sources.search(sourceName, maxCost) #list of found Source objects

    def deleteSource(self, source):
        source.deleted = True

    def findSource(self, sourceName):
        if self.sources != None:
            trie = self.sources
            return trie.search(sourceName, 0)[0][0]

    def findTag(self, tagName):
        if self.tags != None:
            trie = self.tags
            return trie.search(tagName, 0)[0][0]

    def deleteTag(self, tag):
        def delFromSubTags(node):
            if node.item:
                node.item.subTags.deleteItem(tag.name)
        def delFromSuperTags(node):
            if node.item:
                node.item.superTags.deleteItem(tag.name)
        def delFromRelatedTags(node):
            if node.item:
                node.item.relatedTags.deleteItem(tag.name)
        def delFromTags(node):
            if node.item:
                node.item.tags.deleteItem(tag.name)
        super = tag.superTags
        sub = tag.subTags
        related = tag.relatedTags
        sources = tag.sources
        super.traverseInOrder(delFromSubTags)
        sub.traverseInOrder(delFromSuperTags)
        related.traverseInOrder(delFromRelatedTags)
        sources.traverseInOrder(delFromTags)
        self.tags.deleteItem(tag.name)

    def renameTag(self, tag, newName):
        temp = tag
        super = tag.superTags
        sub = tag.subTags
        related = tag.relatedTags
        sources = tag.sources
        self.deleteTag(tag)
        tag.name = newName
        def insertInSubTags(node):
            if node.item:
                node.item.subTags.insert(temp.name, temp)
        def insertInSuperTags(node):
            if node.item:
                node.item.superTags.insert(temp.name, temp)
        def insertInRelatedTags(node):
            if node.item:
                node.item.relatedTags.insert(temp.name, temp)
        def insertInTags(node):
            if node.item:
                node.item.tags.insert(temp.name, temp)
        super.traverseInOrder(insertInSubTags)
        sub.traverseInOrder(insertInSuperTags)
        related.traverseInOrder(insertInRelatedTags)
        sources.traverseInOrder(insertInTags)
        self.addTag(temp)