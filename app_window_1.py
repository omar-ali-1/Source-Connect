from PySide.QtCore import *
from PySide.QtGui import *
from edit_tag_dialog import *
from add_tag_dialog import *
from choose_items_dialog import *
import sys, main_window_qt, source, database, tag, os.path, subprocess, shutil, TrieStructure
import cPickle as pickle


class ChooseItemsDialog(QDialog, Ui_chooseContentDialog):
    def __init__(self, itemTree=None, parent=None):
        super(ChooseItemsDialog, self).__init__(parent)
        self.itemTree = itemTree  # Trie Tree of tags or sources
        self.setupUi(self)
        self.updateDisplayedItems()

    def updateDisplayedItemOperation(self, node):
        item = node.item
        if item and not item.deleted:
            self.chooseItemDialogList.addItem(QListWidgetItem(item.name))

    def updateDisplayedItems(self):
        self.chooseItemDialogList.clear()
        self.itemTree.traverseInOrder(self.updateDisplayedItemOperation)




class AddTagDialog(QDialog, Ui_AddTagDialog):
    def __init__(self, parent=None):
        super(AddTagDialog, self).__init__(parent)
        self.setupUi(self)



class EditTagDialog(QDialog, Ui_editTagDialog):
    def __init__(self, tag=None, database=None, parent=None):
        super(EditTagDialog, self).__init__(parent)
        self.setupUi(self)
        self.tag = tag
        self.database = database
        self.tagNameLineEdit.setText(self.tag.name)
        self.displayedSuperTags = self.tag.superTags
        self.displayedSubTags = self.tag.subTags
        self.displayedRelatedTags = self.tag.relatedTags
        self.displayedSources = self.tag.sources
        self.updateRelatedTagsList()
        self.updateSubtagsList()
        self.updateSources()
        self.updateSupertagsList()

        self.relatedTagAddButton.clicked.connect(self.addRelatedTags)
        self.relatedTagRemoveButton.clicked.connect(self.removeRelatedTags)
        self.subtagAddButton.clicked.connect(self.addSubTags)
        self.subtagRemoveButton.clicked.connect(self.removeSubTags)
        self.supertagAddButton.clicked.connect(self.addSuperTags)
        self.supertagRemoveButton.clicked.connect(self.removeSuperTags)

    def addRelatedTags(self):
        dialog = ChooseItemsDialog(self.database.tags)
        if dialog.exec_():
            selectedTagItems = dialog.chooseItemDialogList.selectedItems()
            for item in selectedTagItems:
                newRelatedTag = self.database.findTag(item.text())
                self.tag.addRelatedTag(newRelatedTag)
            self.updateRelatedTagsList()

    def removeRelatedTags(self):
        selectedRelatedTagItems = self.relatedTagsList.selectedItems()
        for item in selectedRelatedTagItems:
            self.tag.deleteRelatedTag(item.text())
        self.updateRelatedTagsList()

    def addSuperTags(self):
        dialog = ChooseItemsDialog(self.database.tags)
        if dialog.exec_():
            selectedTagItems = dialog.chooseItemDialogList.selectedItems()
            for item in selectedTagItems:
                newSuperTag = self.database.findTag(item.text())
                self.tag.addSuperTag(newSuperTag)
            self.updateSupertagsList()

    def removeSuperTags(self):
        selectedSupertagItems = self.supertagsList.selectedItems()
        for item in selectedSupertagItems:
            self.tag.deleteSuperTag(item.text())
        self.displayedSuperTags = self.tag.superTags
        self.updateSupertagsList()

    def addSubTags(self):
        dialog = ChooseItemsDialog(self.database.tags)
        if dialog.exec_():
            selectedTagItems = dialog.chooseItemDialogList.selectedItems()
            for item in selectedTagItems:
                newSubTag = self.database.findTag(item.text())
                self.tag.addSubTag(newSubTag)
            self.updateSubtagsList()

    def removeSubTags(self):
        selectedRelatedTagItems = self.subTagsList.selectedItems()
        for item in selectedRelatedTagItems:
            self.tag.deleteSubTag(item.text())
        self.updateSubtagsList()




    def addSourceToList(self, node):
        source = node.item
        if source and not source.deleted:
            self.taggedSourcesList.addItem(QListWidgetItem(source.name))

    def updateSources(self):
        self.taggedSourcesList.clear()
        self.displayedSources.traverseInOrder(self.addSourceToList)

    def addRelatedTagToList(self, node):
        relatedTag = node.item
        if relatedTag and not relatedTag.deleted:
            self.relatedTagsList.addItem(QListWidgetItem(relatedTag.name))

    def updateRelatedTagsList(self):
        self.relatedTagsList.clear()
        self.displayedRelatedTags.traverseInOrder(self.addRelatedTagToList)

    def addSupertagToList(self, node):
        superTag = node.item
        if superTag and not superTag.deleted:
            self.supertagsList.addItem(QListWidgetItem(superTag.name))

    def updateSupertagsList(self):
        self.supertagsList.clear()
        self.displayedSuperTags.traverseInOrder(self.addSupertagToList)

    def addSubtagToList(self, node):
        subTag = node.item
        if subTag and not subTag.deleted:
            self.subTagsList.addItem(QListWidgetItem(subTag.name))

    def updateSubtagsList(self):
        self.subTagsList.clear()
        self.displayedSubTags.traverseInOrder(self.addSubtagToList)





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
        ###############################################################################################################
        self.tagListWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.editTagAction = QAction("Edit Tag (select only one)", None)
        self.editTagAction.triggered.connect(self.editTag)
        self.tagListWidget.addAction(self.editTagAction)

        self.addTagAction = QAction("Add Tag", None)
        self.addTagAction.triggered.connect(self.addTag)
        self.tagListWidget.addAction(self.addTagAction)
        ###############################################################################################################
        self.connect(self.sourceContentSearchButton, SIGNAL('clicked()'), self.updateSourceContentList)
        self.connect(self.loadDatabaseAction, SIGNAL('triggered()'), self.loadDatabase)
        self.newDatabaseAction.triggered.connect(self.createDatabase)
        self.connect(self.tagListWidget, SIGNAL('itemSelectionChanged()'), self.tagsSelected)
        self.connect(self.sourcesList, SIGNAL('itemSelectionChanged()'), self.sourcesSelected)
        # new connection style
        self.sourceContentList.itemDoubleClicked.connect(self.openItem)
        self.connect(self.tagSearchButton, SIGNAL('clicked()'), self.tagListWidget.clearSelection)
        self.connect(self.sourcesSearchButton, SIGNAL('clicked()'), self.sourcesList.clear)

    def addTag(self):
        addTagDialog = AddTagDialog()
        if addTagDialog.exec_():
            newTagName = addTagDialog.addTagLineEdit.text()
            if newTagName:
                newTag = tag.Tag(newTagName)
                self.database.addTag(newTag)
                self.updateTagsList()

    def editTag(self):
        selectedTagItems = self.tagListWidget.selectedItems()
        if len(selectedTagItems) == 1:
            selectedTagName = selectedTagItems[0].text()
            selectedTag = self.findDisplayedTag(selectedTagName)
            editTagDialog = EditTagDialog(selectedTag, self.database)
            editTagDialog.exec_()
            text = editTagDialog.tagNameLineEdit.text()
            if text != selectedTag.name:
                self.database.renameTag(selectedTag, text)
            self.updateTagsList()

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

    def insertSourceOperation(self, node):
        if node.item and node.item.deleted == False:
            self.displayedSources.insert(node.item.name, node.item)

    def tagsSelected(self):
        selectedTags = []
        selectedTagItems = self.tagListWidget.selectedItems()
        for tagItem in selectedTagItems:
            selectedTags.append(self.findDisplayedTag(tagItem.text()))
        if len(selectedTags) == 0:
            self.displayedSources = self.database.sources
        else:
            self.displayedSources = TrieStructure.TrieTree()
            for tag in selectedTags:
                tag.sources.traverseInOrder(self.insertSourceOperation)
        self.updateSourcesList()

    def sourcesSelected(self):
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
        else:
            self.sourceTextBrowser.clear()

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
            trie = self.displayedTags
            return trie.search(tagName, 0)[0][0]

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