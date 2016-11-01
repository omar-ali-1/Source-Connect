#from PIL import Image

import os, shutil, TrieStructure

class Source(object):
    """docstring for ClassName"""
    def __init__(self, name, location):
        self.name = name  # string
        self.deleted = False
        self.location = location  # string
        self.tags = TrieStructure.TrieTree()  # array of Tag objects

    def addTag(self, tag):
        self.tags.insert(tag.name, tag)

    def getContentList(self):
        # returns list of tuples: file name, file absolute path
        path = self.location.replace('\\', '\\\\')
        contents = []
        for dirPath, subDirs, files in os.walk(path):
            for f in files:
                contents.append((f, dirPath + f))
            return contents

    def getTags(self):
        return self.tags

    def getLocation(self):
        return self.location

