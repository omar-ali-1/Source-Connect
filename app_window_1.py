from PySide.QtCore import *
from PySide.QtGui import *
import sys, main_window_qt, source, database, tag, os.path, subprocess
import cPickle as pickle


class MainAppWindow(QMainWindow, main_window_qt.Ui_sourceConnectMainWindow):
    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        self.setupUi(self)
        self.item = QListWidgetItem("hey there mr billy!")
        self.databasePath = None
        self.database = None

        self.tagListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sourcesList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.connect(self.sourceContentSearchButton, SIGNAL('clicked()'), self.updateSourceContentList)
        self.connect(self.loadDatabaseAction, SIGNAL('triggered()'), self.loadDatabase)
        self.newDatabaseAction.triggered.connect(self.createDatabase)
        self.connect(self.tagListWidget, SIGNAL('itemSelectionChanged()'), self.updateSourcesList)
        self.connect(self.sourcesList, SIGNAL('itemSelectionChanged()'), self.updateSourceContentList)
        # new connection style
        self.sourceContentList.itemDoubleClicked.connect(self.openItem)
        self.sourcesList.itemSelectionChanged.connect(self.displaySummary)
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
        newDatabaseName = QFileDialog.getSaveFileName(self)
        print newDatabaseName

    def displaySummary(self):
        selectedSourceItems = self.sourcesList.selectedItems()
        if len(selectedSourceItems) == 1:
            sourceItem = selectedSourceItems[0]
            selectedSource = self.findSource(sourceItem.text())
            self.sourceTextBrowser.setSource(QUrl.fromLocalFile(self.database.directory + '\\' + selectedSource.location \
                                             + '\\' + "summary.html"))

    def openItem(self, sourceContentItem):
        selectedSourceItems = self.sourcesList.selectedItems()
        for selectedSourceItem in selectedSourceItems:
            source = self.findSource(selectedSourceItem.text())
            for path, directories, files in os.walk(self.database.directory + '\\' + source.location ):
                for file in files:
                    if file == sourceContentItem.text():
                        subprocess.Popen([self.database.directory + '\\' + source.location + '\\' + file], shell=True)


    def findTag(self, tagName):
        for tag in self.database.tags:
            if tagName == tag.name:
                return tag

    def findSource(self, sourceName):
        for source in self.database.sources:
            if sourceName == source.title:
                return source

    def updateSourceContentList(self):
        self.sourceContentList.clear()
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

    def updateSourcesList(self):
        self.sourcesList.clear()
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

    def loadDatabase(self):
        systemFileExists = False
        self.databasePath = QFileDialog.getExistingDirectory(self)
        for path, dirs, files in os.walk(self.databasePath):
            for file in files:
                if file == "systemFile.p": systemFileExists = True
        if not systemFileExists:
            newDataBase = database.Database(self.databasePath.split("\\")[-1])
            pickle.dump(newDataBase, open(self.databasePath + "\\systemFile.p", "wb"))
        self.database = pickle.load(open(self.databasePath + "\\systemFile.p", "rb"))
        # print self.databaseName
        self.updateTagsList()
        self.updateSourcesList()
