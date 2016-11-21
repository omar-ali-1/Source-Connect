# coding: utf-8
from PySide.QtCore import *
from PySide.QtGui import *
from edit_tag_dialog import *
from add_tag_dialog import *
from add_source_dialog import *
from edit_source_dialog import *
from choose_items_dialog import *
import sys, main_window_qt, source, database, tag, os.path, subprocess, shutil, TrieStructure
import cPickle as pickle
import operator
#from django.utils.encoding import smart_str, smart_unicode
#from PySide.QtWebKit import *
#import chardet
# import docx2html
sys.setrecursionlimit(30000)

class ChooseItemsDialog(QDialog, Ui_chooseContentDialog):
    def __init__(self, itemTree=None, parent=None):
        super(ChooseItemsDialog, self).__init__(parent)
        self.itemTree = itemTree  # Trie Tree of tags or sources
        self.setupUi(self)
        self.updateDisplayedItems()
        self.chooseItemDialogLineEdit.textChanged.connect(self.search)

    def search(self):
        text = self.chooseItemDialogLineEdit.text()
        if text == '' or text == None:
            self.updateDisplayedItems()
        else:
            results = sorted(self.itemTree.search(text, 25), key = operator.itemgetter(1, 0))
            self.chooseItemDialogList.clear()
            for tuple in results:
                self.chooseItemDialogList.addItem(QListWidgetItem(tuple[0].name))


    def updateDisplayedItemOperation(self, node):
        item = node.item
        if item and not item.deleted:
            self.chooseItemDialogList.addItem(QListWidgetItem(item.name))

    def updateDisplayedItems(self):
        self.chooseItemDialogList.clear()
        self.itemTree.traverseInOrder(self.updateDisplayedItemOperation)


class AddSourceDialog(QDialog, Ui_AddSourceDialog):
    def __init__(self, parent=None):
        super(AddSourceDialog, self).__init__(parent)
        self.setupUi(self)


class EditSourceDialog(QDialog, Ui_editSourceDialog):   # continue here
    def __init__(self, source=None, database=None, parent=None):
        super(EditSourceDialog, self).__init__(parent)
        self.setupUi(self)
        self.source = source
        self.database = database
        self.sourceNameLineEdit.setText(self.source.name)
        self.displayedTags= self.source.tags
        self.displayedFiles = self.source.getContentList()

        self.updateTagsList()
        self.updateFilesList()

        self.tagAddButton.clicked.connect(self.addTags)
        self.tagRemoveButton.clicked.connect(self.removeTags)
        self.fileAddButton.clicked.connect(self.addFiles)
        self.fileRemoveButton.clicked.connect(self.removeFiles)
        self.tagLineEdit.textChanged.connect(self.searchTags)
        self.tagLineEdit.textChanged.connect(self.searchTags)  # needs implementation since files not stored in tree

    def searchTags(self):
        text = self.tagLineEdit.text()
        if text == '' or text == None:
            self.updateTagsList()
        else:
            results = sorted(self.displayedTags.search(text, 25), key=operator.itemgetter(1, 0))
            self.tagsList.clear()
            for tuple in results:
                self.tagsList.addItem(QListWidgetItem(tuple[0].name))

    def addTags(self):
        dialog = ChooseItemsDialog(self.database.tags)
        if dialog.exec_():
            selectedTagItems = dialog.chooseItemDialogList.selectedItems()
            for item in selectedTagItems:
                newTag= self.database.findTag(item.text())
                self.source.addTag(newTag)
            self.updateTagsList()

    def removeTags(self):
        selectedTagItems = self.tagsList.selectedItems()
        for item in selectedTagItems:
            self.source.deleteTag(item.text())
        self.updateTagsList()

    def addFiles(self):
        filePathsAndNames = QFileDialog.getOpenFileNames(self)
        for filePathAndName in filePathsAndNames[0]:
            self.source.addFile(filePathAndName)
        self.updateFilesList()

    def removeFiles(self):
        selectedFileItems = self.fileList.selectedItems()
        for item in selectedFileItems:
            self.source.deleteFile(item.text())
        self.updateFilesList()

    def updateFilesList(self):
        self.fileList.clear()
        for path, directories, files in os.walk(self.database.path + '\\' + self.source.locationRelToDatabase):
            for file in files:
                self.fileList.addItem(QListWidgetItem(file))

    def addTagToList(self, node):
        tag = node.item
        if tag and not tag.deleted:
            self.tagsList.addItem(QListWidgetItem(tag.name))

    def updateTagsList(self):
        self.tagsList.clear()
        self.displayedTags.traverseInOrder(self.addTagToList)




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
        self.taggedSourceAddButton.clicked.connect(self.addTaggedSource)
        self.taggedSourceRemoveButton.clicked.connect(self.removeTaggedSource)
        self.supertagsLineEdit.textChanged.connect(self.searchSuperTags)
        self.subtagsLineEdit.textChanged.connect(self.searchSubTags)
        self.relatedTagsLineEdit.textChanged.connect(self.searchRelatedTags)
        self.taggedSourcesLineEdit.textChanged.connect(self.searchSources)

    def searchSuperTags(self):
        text = self.supertagsLineEdit.text()
        if text == '' or text == None:
            self.updateSupertagsList()
        else:
            results = sorted(self.displayedSuperTags.search(text, 25), key=operator.itemgetter(1, 0))
            self.supertagsList.clear()
            for tuple in results:
                self.supertagsList.addItem(QListWidgetItem(tuple[0].name))

    def searchSubTags(self):
        text = self.subtagsLineEdit.text()
        if text == '' or text == None:
            self.updateSubtagsList()
        else:
            results = sorted(self.displayedSubTags.search(text, 25), key=operator.itemgetter(1, 0))
            self.subTagsList.clear()
            for tuple in results:
                self.subTagsList.addItem(QListWidgetItem(tuple[0].name))

    def searchRelatedTags(self):
        text = self.relatedTagsLineEdit.text()
        if text == '' or text == None:
            self.updateRelatedTagsList()
        else:
            results = sorted(self.displayedRelatedTags.search(text, 25), key=operator.itemgetter(1, 0))
            self.relatedTagsList.clear()
            for tuple in results:
                self.relatedTagsList.addItem(QListWidgetItem(tuple[0].name))

    def searchSources(self):
        text = self.taggedSourcesLineEdit.text()
        if text == '' or text == None:
            self.updateSources()
        else:
            results = sorted(self.displayedSources.search(text, 25), key=operator.itemgetter(1, 0))
            self.taggedSourcesList.clear()
            for tuple in results:
                self.taggedSourcesList.addItem(QListWidgetItem(tuple[0].name))

    def addTaggedSource(self):
        dialog = ChooseItemsDialog(self.database.sources)
        if dialog.exec_():
            selectedSourceItems = dialog.chooseItemDialogList.selectedItems()
            for item in selectedSourceItems:
                newTaggedSource = self.database.findSource(item.text())
                self.tag.addSource(newTaggedSource)
            self.updateSources()

    def removeTaggedSource(self):
        selectedTaggedSourceItems = self.taggedSourcesList.selectedItems()
        for item in selectedTaggedSourceItems:
            self.tag.deleteTaggedSource(item.text())
        self.updateSources()

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
        self.summary = None
        self.sourceTextBrowser.setOpenExternalLinks(True)

        self.setupSourceTree()
        self.setupTagList()
        self.setupTextBrowser()
        self.setupActionMenu()


    def setupActionMenu(self):
        self.connect(self.loadDatabaseAction, SIGNAL('triggered()'), self.loadDatabase)
        self.newDatabaseAction.triggered.connect(self.createDatabase)
        #self.sourceContentList.itemDoubleClicked.connect(self.openItem)
        self.saveToDatabaseAction.triggered.connect(self.saveChangesToCurrentDatabase)

    def setupTextBrowser(self):
        #cursor = QTextCursor()
        #self.sourceTextBrowser.setTextCursor(cursor)
        self.sourceTextBrowser.textChanged.connect(self.summaryEdited)
        self.saveButton.clicked.connect(self.saveSummary)
        self.sourceTextBrowser.setReadOnly(False)
        self.saveToDatabaseAction.triggered.connect(self.saveSummary)
        self.italicButton.clicked.connect(self.italicClicked)
        self.boldButton.clicked.connect(self.boldClicked)
        self.underlineButton.clicked.connect(self.underlineClicked)

    def italicClicked(self):
        cursor = self.sourceTextBrowser.textCursor()
        isItalic = self.sourceTextBrowser.fontItalic()
        fmt = QTextCharFormat()
        fmt.setFontItalic(not isItalic)
        cursor.mergeCharFormat(fmt)
        self.sourceTextBrowser.mergeCurrentCharFormat(fmt)

    def boldClicked(self):
        cursor = self.sourceTextBrowser.textCursor()
        isBold = self.sourceTextBrowser.fontWeight() > QFont.Normal
        fmt = QTextCharFormat()
        if not isBold:
            fmt.setFontWeight(QFont.Bold)
        else:
            fmt.setFontWeight(QFont.Normal)
        cursor.mergeCharFormat(fmt)
        self.sourceTextBrowser.mergeCurrentCharFormat(fmt)

    def underlineClicked(self):
        cursor = self.sourceTextBrowser.textCursor()
        isUnderlined = self.sourceTextBrowser.fontUnderline()
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not isUnderlined)
        cursor.mergeCharFormat(fmt)
        self.sourceTextBrowser.mergeCurrentCharFormat(fmt)

    def setupTagList(self):
        self.tagListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tagListWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.editTagAction = QAction("Edit Tag (select only one)", None)
        self.editTagAction.triggered.connect(self.editTag)
        self.tagListWidget.addAction(self.editTagAction)

        self.addTagAction = QAction("Add Tag", None)
        self.addTagAction.triggered.connect(self.addTag)
        self.tagListWidget.addAction(self.addTagAction)

        self.deleteTagsAction = QAction("Delete Tag(s) (permanent)", None)
        self.deleteTagsAction.triggered.connect(self.deleteTags)
        self.tagListWidget.addAction(self.deleteTagsAction)

        self.connect(self.tagListWidget, SIGNAL('itemSelectionChanged()'), self.tagsSelected)
        self.clearTagsButton.clicked.connect(self.tagListWidget.clearSelection)
        self.superTagButton.clicked.connect(self.superTagsRequested)
        self.subTagButton.clicked.connect(self.subTagsRequested)
        self.allTagsButton.clicked.connect(self.allTagsRequested)
        self.tagListWidget.itemDoubleClicked.connect(self.subTagsRequested)
        self.tagLineEdit.textChanged.connect(self.searchTags)
        self.tagListWidget.itemDoubleClicked.connect(self.subTagsRequested)

    def setupSourceTree(self):
        self.sourceLineEdit.textChanged.connect(self.searchSources)
        self.connect(self.sourcesList, SIGNAL('itemSelectionChanged()'), self.displaySummary)
        self.sourcesList.itemDoubleClicked.connect(self.openItem)

        self.sourcesList.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.editSourceAction = QAction("Edit Source (select only one)", None)
        self.editSourceAction.triggered.connect(self.editSource)
        self.sourcesList.addAction(self.editSourceAction)

        self.addSourceAction = QAction("Add Source", None)
        self.addSourceAction.triggered.connect(self.addSource)
        self.sourcesList.addAction(self.addSourceAction)

        self.deleteSourcesAction = QAction("Delete Source(s) (permanent)", None)
        self.deleteSourcesAction.triggered.connect(self.deleteSources)
        self.sourcesList.addAction(self.deleteSourcesAction)

    def superTagsRequested(self):
        newDisplayedTags = TrieStructure.TrieTree()
        selectedTagItems = self.tagListWidget.selectedItems()
        if len(selectedTagItems) == 0:
            return
        def insertOperation(node):
            newDisplayedTags.insert(node.item.name, node.item)

        for item in selectedTagItems:
            tag = self.findDisplayedTag(item.text())
            tag.superTags.traverseInOrder(insertOperation)
        self.displayedTags = newDisplayedTags
        self.updateTagsList()


    def subTagsRequested(self):
        newDisplayedTags = TrieStructure.TrieTree()
        selectedTagItems = self.tagListWidget.selectedItems()
        if len(selectedTagItems) == 0:
            return

        def insertOperation(node):

            newDisplayedTags.insert(node.item.name, node.item)

        for item in selectedTagItems:
            tag = self.findDisplayedTag(item.text())
            tag.subTags.traverseInOrder(insertOperation)
        if newDisplayedTags.nodeCount > 1:
            self.displayedTags = newDisplayedTags
            self.updateTagsList()

    def allTagsRequested(self):
        self.displayedTags = self.database.tags
        self.updateTagsList()


    def searchTags(self):
        text = self.tagLineEdit.text()
        if text == '' or text == None:
            self.updateTagsList()
        else:
            results = sorted(self.displayedTags.search(text, 25), key=operator.itemgetter(1, 0))
            self.tagListWidget.clear()
            for tuple in results:
                self.tagListWidget.addItem(QListWidgetItem(tuple[0].name))

    def searchSources(self):
        text = self.sourceLineEdit.text()
        if text == '' or text == None:
            self.updateSourcesList()
        else:
            results = sorted(self.displayedSources.search(text, 25), key=operator.itemgetter(1, 0))
            self.sourcesList.clear()
            for tuple in results:
                source = tuple[0]
                item = QTreeWidgetItem(self.sourcesList)
                item.setText(0, source.name)
                for path, dirs, files in os.walk(self.database.path + '\\' + source.locationRelToDatabase):
                    for file in files:
                        child = QTreeWidgetItem(item)
                        child.setText(0, file)

    def addSource(self):
        addSourceDialog = AddSourceDialog()
        if addSourceDialog.exec_():
            newSourceName = addSourceDialog.addSourceLineEdit.text()
            if newSourceName:
                newSource = source.Source(newSourceName, self.database)
                self.database.addSourceObjectOnly(newSource)
                self.updateSourcesList()
        #self.saveChangesToCurrentDatabase()

    def editSource(self):
        selectedSourceItems = self.sourcesList.selectedItems()
        if len(selectedSourceItems) == 1:
            selectedSourceName = selectedSourceItems[0].text(0)
            selectedSource = self.findDisplayedSource(selectedSourceName)
            editSourceDialog = EditSourceDialog(selectedSource, self.database)
            editSourceDialog.exec_()
            text = editSourceDialog.sourceNameLineEdit.text()
            if text != selectedSource.name:
                self.database.renameSource(selectedSource, text)
            self.updateSourcesList()
        #self.saveChangesToCurrentDatabase()

    def deleteSources(self):
        selectedSourceItems = self.sourcesList.selectedItems()
        for item in selectedSourceItems:
            self.database.deleteSource(self.database.findSource(item.text(0)))
        self.updateSourcesList()

    def addTag(self):
        addTagDialog = AddTagDialog()
        if addTagDialog.exec_():
            newTagName = addTagDialog.addTagLineEdit.text()
            if newTagName:
                newTag = tag.Tag(newTagName)
                self.database.addTag(newTag)
                self.updateTagsList()
        #self.saveChangesToCurrentDatabase()

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
            #self.saveChangesToCurrentDatabase()

    def deleteTags(self):
        selectedTagItems = self.tagListWidget.selectedItems()
        for item in selectedTagItems:
            self.database.deleteTag(self.database.findTag(item.text()))
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
        self.sourcesList.clearSelection()
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


    # a bug needs to be fixed: when selecting a source with no tags selected, and its summary is displayed, then when
    # a tag is selected, an error is raised :
    # return trie.search(sourceName, 0)[0][0]
    # IndexError: list index out of range

    def displaySummary(self): #should contain one source
        #print self.sourcesList.selectedItems()[0].text(0)
        if len(self.sourcesList.selectedItems()) > 0:
            sourceItem = self.sourcesList.selectedItems()[0]
        else:
            self.sourceTextBrowser.clear()
            return
        if sourceItem.parent() is not None:
            sourceItem = sourceItem.parent()
        selectedSource = self.findDisplayedSource(sourceItem.text(0))
        if selectedSource:
            self.summary = self.database.path + '\\' + selectedSource.locationRelToDatabase + '\\' + "summary.html"
            summaryFile = open(self.summary, 'r')
            self.summaryHTML = summaryFile.read().decode("utf-8")
            self.sourceTextBrowser.setHtml(self.summaryHTML)
            summaryFile.close()

    def saveSummary(self):
        summaryFile = open(self.summary, 'w')
        #encoding = chardet.detect(self.summaryHTML)

        summaryFile.write(self.summaryHTML.encode("utf-8"))
        summaryFile.close()

    def summaryEdited(self):
        self.summaryHTML = self.sourceTextBrowser.toHtml()

    def updateSourceContentList(self, selectedSources):
        self.sourceContentList.clear()
        for source in selectedSources:
            for path, directories, files in os.walk(self.databasePath + '\\' + source.locationRelToDatabase):
                for file in files:
                    if file != 'summary.html':
                        self.sourceContentList.addItem(QListWidgetItem(file))

    def openItem(self):
        selectedSourceTreeItems = self.sourcesList.selectedItems()
        selectedItem = selectedSourceTreeItems[0]
        if selectedItem.parent() is None:
            return

        source = self.findDisplayedSource(selectedItem.parent().text(0))
        for path, directories, files in os.walk(self.databasePath + '\\' + source.locationRelToDatabase ):
            for file in files:
                if file == selectedItem.text(0):
                    subprocess.Popen([self.databasePath + '\\' + source.locationRelToDatabase + '\\' + file], shell=True)


    def findDisplayedSource(self, sourceName):
        if self.displayedSources != None:
            trie = self.database.sources
            result = trie.search(sourceName, 0)
            return result[0][0]

    def findDisplayedTag(self, tagName):
        if self.displayedTags != None:
            trie = self.displayedTags
            return trie.search(tagName, 0)[0][0]

# continue here make sure update works and implement search functions


    def updateSourceOperation(self, node):
        source = node.item
        if source and not source.deleted:
            item = QTreeWidgetItem(self.sourcesList)
            item.setText(0, source.name)
            children = []
            for path, dirs, files in os.walk(self.database.path + '\\' + source.locationRelToDatabase):
                for file in files:
                    child = QTreeWidgetItem(item)
                    child.setText(0, file)
                    #children.append(QTreeWidgetItem(file))
            #item.addChildren(children)
            #self.sourcesList.addItem(item)

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
                if file == "systemFile.p":
                    systemFileExists = True
                    break
                #print systemFileExists
        if not systemFileExists:
            newDataBase = database.Database(self.databasePath.split("\\")[-1], self.databasePath)
            pickle.dump(newDataBase, open(self.databasePath + "\\systemFile.p", "wb"))
        self.database = pickle.load(open(self.databasePath + "\\systemFile.p", "rb"))
        self.database.updatePath(self.databasePath)
        #print self.database.name

        self.displayedSources = self.database.sources
        self.displayedTags = self.database.tags
        #self.displayedTags.printTree()
        #self.displayedSources.printTree()
        self.updateTagsList()
        self.updateSourcesList()

    def saveChangesToCurrentDatabase(self):
        pickle.dump(self.database, open(self.databasePath + "\\systemFile.p", "wb"))