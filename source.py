#from PIL import Image

import os, shutil, TrieStructure

class Source(object):
    """docstring for ClassName"""
    def __init__(self, name, database):
        self.name = name  # string
        self.deleted = False
        self.database = database # string
        self.locationRelToDatabase = None
        self.createLocation(database.path)
        self.tags = TrieStructure.TrieTree()  # array of Tag objects
        self.addSummary()

    def addSummary(self):
        if not os.path.isfile(self.database.path + '\\' + self.locationRelToDatabase + '\\' + 'summary.html'):
            summary = open(self.database.path + '\\' + self.locationRelToDatabase + '\\' + 'summary.html', 'w')
            summary.close()


    def createLocation(self, path):
        i = 0
        while os.path.exists(path + '\\\\' + str(i)):
            i += 1
        os.makedirs(path + '\\\\' + str(i))
        self.locationRelToDatabase = str(i)

    def addFile(self, pathOfFile):
        shutil.copy(pathOfFile, self.database.path + '\\' + self.locationRelToDatabase)

    def deleteFile(self, fileName):
        os.remove(self.database.path + '\\\\' + self.locationRelToDatabase + '\\\\' + fileName)

    def addTag(self, tag):
        self.tags.insert(tag.name, tag)
        tag.sources.insert(self.name, self)

    def deleteTag(self, tagName):
        tag = self.tags.search(tagName, 0)[0][0]
        self.tags.deleteItem(tagName)
        tag.sources.deleteItem(self.name)

    def getContentList(self):
        # returns list of tuples: file name, file absolute path
        path = self.locationRelToDatabase.replace('\\', '\\\\')
        contents = []
        for dirPath, subDirs, files in os.walk(path):
            for f in files:
                contents.append((f, dirPath + f))
            return contents



    def getTags(self):
        return self.tags

    def getLocation(self):
        return self.locationRelToDatabase

