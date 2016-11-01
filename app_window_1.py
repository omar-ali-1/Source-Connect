from PySide.QtCore import *
from PySide.QtGui import *
import sys, main_window_qt, source, database, tag, os.path, subprocess, shutil
import cPickle as pickle


class MainAppWindow(QMainWindow, main_window_qt.Ui_sourceConnectMainWindow):
    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        self.setupUi(self)
        self.databasePath = None
        self.database = None
        self.displayedTags = None
        self.displayedSources = None

        self.tagListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sourcesList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.connect(self.sourceContentSearchButton, SIGNAL('clicked()'), self.updateSourceContentList)
        self.connect(self.loadDatabaseAction, SIGNAL('triggered()'), self.loadDatabase)
        self.newDatabaseAction.triggered.connect(self.createDatabase)
        self.connect(self.tagListWidget, SIGNAL('itemSelectionChanged()'), self.updateSourcesList)
        self.connect(self.sourcesList, SIGNAL('itemSelectionChanged()'), self.sourceSelected)
        # new connection style
        self.sourceContentList.itemDoubleClicked.connect(self.openItem)
        self.connect(self.tagSearchButton, SIGNAL('clicked()'), self.tagListWidget.clearSelection)
        self.connect(self.sourcesSearchButton, SIGNAL('clicked()'), self.sourcesList.clear)

    def createDatabase(self):
        msgBox = QMessageBox()
        msgBox.setText("To create a new database, simply create an empty new folder anywhere on your computer, name it, "
                       "then load it like you would an existing database.")
        #msgBox.setInformativeText("Do you want to save your changes?")
        #msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        #msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec_()
        #newDatabaseName = QFileDialog.getSaveFileName(self)
        #print newDatabaseName

    def sourceSelected(self):
        selectedSources = []
        selectedSourceItems = self.sourcesList.selectedItems()
        for sourceItem in selectedSourceItems:
            selectedSources.append(self.findDisplayedSource(sourceItem.text()))
        self.displaySummary(selectedSources)
        self.updateSourceContentList(selectedSources)

    def displaySummary(self, selectedSources): #should contain one source
        if len(selectedSources) == 1:
            selectedSource = selectedSources[0]
            #print selectedSources
            self.sourceTextBrowser.setSource(QUrl.fromLocalFile(self.databasePath + '\\' + \
                                                                selectedSource.location + '\\' + "summary.html"))

    def updateSourceContentList(self, selectedSources):
        self.sourceContentList.clear()
        for source in selectedSources:
            for path, directories, files in os.walk(self.databasePath + '\\' + source.location):
                for file in files:
                    self.sourceContentList.addItem(QListWidgetItem(file))
        '''
        sourceContentName = self.sourceContentLineEdit.text()
        selectedSourceItems = self.sourcesList.selectedItems()
        if (sourceContentName == None or sourceContentName == ""):
            for sourceItem in selectedSourceItems:
                source = self.findSource(sourceItem.text())
                for path, directories, files in os.walk(self.database.directory + '\\' + source.location):
                    for file in files:
                        self.sourceContentList.addItem(QListWidgetItem(file))
        else:
            for sourceItem in selectedSourceItems:
                source = self.findSource(sourceItem.text())
                for path, directories, files in os.walk(self.database.directory + '\\' + source.location):
                    for file in files:
                        if file == sourceContentName:
                            self.sourceContentList.addItem(QListWidgetItem(file.split))
        '''

    def openItem(self, sourceContentItem):
        selectedSourceItems = self.sourcesList.selectedItems()
        for selectedSourceItem in selectedSourceItems:
            source = self.findDisplayedSource(selectedSourceItem.text())
            for path, directories, files in os.walk(self.databasePath + '\\' + source.location ):
                for file in files:
                    if file == sourceContentItem.text():
                        subprocess.Popen([self.databasePath + '\\' + source.location + '\\' + file], shell=True)

    def deleteSource(self, source):
        source.deleted = True
        shutil.rmtree(self.databasePath + '\\' + source.location)

    def deleteTag(self, tag):
        tag.deleted = True


    def findDisplayedSource(self, sourceName):
        if self.displayedSources != None:
            trie = self.displayedSources
            return trie.search(sourceName, 0)[0][0]

    def findDisplayedTag(self, tagName):
        if self.displayedTags != None:
            node = self.displayedTags
            for letter in tagName:
                if letter in node.children:
                    node = node.children[letter]
            return node.item

# continue here make sure update works and implement search functions


    def updateSourceOperation(self, node):
        source = node.item
        if source and not source.deleted:
            self.sourcesList.addItem(QListWidgetItem(source.name))

    def updateSourcesList(self):
        self.sourcesList.clear()
        self.displayedSources.traverseInOrder(self.updateSourceOperation)

    def updateTagOperation(self, node):
        tag = node.item
        #print tag
        if tag and not tag.deleted:
            self.tagListWidget.addItem(QListWidgetItem(tag.name))

    def updateTagsList(self):
        self.tagListWidget.clear()
        self.displayedTags.traverseInOrder(self.updateTagOperation)

    def loadDatabase(self):
        systemFileExists = False
        #print 'here'
        self.databasePath = QFileDialog.getExistingDirectory(self)
        for path, dirs, files in os.walk(self.databasePath):
            for file in files:
                if file == "systemFile.p": systemFileExists = True
                #print systemFileExists
        if not systemFileExists:
            newDataBase = database.Database(self.databasePath.split("\\")[-1])
            pickle.dump(newDataBase, open(self.databasePath + "\\systemFile.p", "wb"))
        self.database = pickle.load(open(self.databasePath + "\\systemFile.p", "rb"))
        #print self.database.name

        self.displayedSources = self.database.sources
        self.displayedTags = self.database.tags
        #self.displayedTags.printTree()
        #self.displayedSources.printTree()
        self.updateTagsList()
        self.updateSourcesList()

    def printt(selfs, obj):
        print obj

'''
        sourceName = self.sourceLineEdit.text()
        selectedTagListItems = self.tagListWidget.selectedItems()
        if (sourceName == None or sourceName == "") and self.database != None:
            for selectedTagListItem in selectedTagListItems:
                selectedTagName = selectedTagListItem.text()
                tag = self.findTag(selectedTagName)
                for s in tag.sources:
                    self.sourcesList.addItem(QListWidgetItem(s.title))
            if not selectedTagListItems:
                for i in xrange(len(self.database.sources)):
                    self.sourcesList.addItem(QListWidgetItem(self.database.sources[i].title))
        elif self.database:
            for selectedTagListItem in selectedTagListItems:
                selectedTagName = selectedTagListItem.text()
                tag = self.findTag(selectedTagName)
                for s in tag.sources:
                    if s.title == sourceName:
                        self.sourcesList.addItem(QListWidgetItem(s.title))
            if not selectedTagListItems:
                for i in xrange(len(self.database.sources)):
                    if self.database.sources[i].title == sourceName:
                        self.sourcesList.addItem(QListWidgetItem(self.database.sources[i].title))
'''