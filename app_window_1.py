from PySide.QtCore import *
from PySide.QtGui import *
import sys, main_window_qt, source, database, tag
import cPickle as pickle

class MainAppWindow(QMainWindow, main_window_qt.Ui_sourceConnectMainWindow):

    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        self.setupUi(self)
        self.item = QListWidgetItem("hey there mr billy!")
        self.databaseName = None
        self.database = None
        self.connect(self.sourceContentSearchButton, SIGNAL('clicked()'), self.updateSourceContentList)
        self.connect(self.actionLoad_Database, SIGNAL('triggered()'), self.loadDatabase)


    def updateSourceContentList(self):
        self.sourceContentList.clear()
        sourceName = self.sourceContentLineEdit.text()
        if (sourceName == None or sourceName == "") and self.database:
            db = self.database
            for i in xrange(len(self.database.sources)):
                self.sourceContentList.addItem(QListWidgetItem(contents[i][0]))
        source = self.findSource(sourceName)
        contents = source.getContentList()
        for i in xrange(len(contents)):
            self.sourceContentList.addItem(QListWidgetItem(contents[i][0]))

    def updateSourcesList(self):
        self.sourcesList.clear()
        sourceName = self.sourceLineEdit.text()
        if (sourceName == None or sourceName == "") and self.database != None:
            for i in xrange(len(self.database.sources)):
                self.sourcesList.addItem(QListWidgetItem(self.database.sources[i].title))
        elif self.database != None:
            for i in xrange(len(self.database.sources)):
                if self.database.sources[i].title == sourceName:
                    self.sourcesList.addItem(QListWidgetItem(self.database.sources[i].title))

    def updateTagsList(self):
        self.tagListWidget.clear()
        tagName = self.tagLineEdit.text()
        if (tagName == None or tagName == "") and self.database != None:
            for i in xrange(len(self.database.tags)):
                self.tagListWidget.addItem(QListWidgetItem(self.database.tags[i].name))
        elif self.database != None:
            for i in xrange(len(self.database.tags)):
                if self.database.tags[i].name == tagName:
                    self.tagListWidget.addItem(QListWidgetItem(self.database.tags[i].name))


    def findSource(self, sourceName):
        test = source.Source("Iraq", 'C:\Users\OmarAli\Google Drive\Research\SimpleResearch\simple-research\Iraq')
        return test

    def loadDatabase(self):
        self.databaseName = QFileDialog.getExistingDirectory(self)
        self.database = pickle.load(open(self.databaseName + "\\systemFile.p", "rb"))
        #print self.databaseName
        self.updateTagsList()
        self.updateSourcesList()





