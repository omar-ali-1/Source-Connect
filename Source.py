#from PIL import Image
import os

class Source(object):
    """docstring for ClassName"""
    def __init__(self, title, location, tags=None):
        self.title = title  # string
        self.location = location  # string
        self.tags = tags or []  # array of Tag objects
        self.images = [] # array of strings of image names
        self.pdfs = [] # array of strings of pdf names

    def addTag(self, tag):
        self.tags.append(tag)

    def getContentList(self):
        # returns list of tuples: file name, file absolute path
        path = self.location.replace('\\', '\\\\')
        contents = []
        for dirPath, subDirs, files in os.walk(path):
            for f in files:
                contents.append((f, dirPath + f))
            return contents

    def printTags(self):
        for tag in self.tags:
            print tag.name + " "
        print "/"

    def getTags(self):
        return self.tags

    def getLocation(self):
        return self.location

    def addImage(self, name): # name is string including extension
        self.images.append(name)

    def openImages(self, imageList=None):
        imageList = imageList or []
        for image in imageList:
            os.system("start" + self.location + "/Images/" + image)
        if not imageList:
            pass#for images in image folder if it exists, open

    def openPDF(self, pdfList=None):
        if not pdfList:
            return "No PDF files to show."
        for pdfFileName in pdfList:
            os.system("start" + self.location + "/PDFs/" + pdfFileName)
            #subprocess.Popen([self.location + "/PDFs/" + image], shell=True)
