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
