from PySide.QtCore import *
from PySide.QtGui import *
import sys, main_window_qt, source, database, tag

class MainAppWindow(QMainWindow, main_window_qt.Ui_sourceConnectMainWindow):

    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        self.setupUi(self)
        self.connect(self.sourceContentSearchButton, SIGNAL('clicked()'), self.updateSourceContentList)
        self.item = QListWidgetItem("hey there mr billy!")

    def updateSourceContentList(self):
        self.sourceContentList.clear()
        sourceName = self.sourceContentLineEdit.text()
        source = self.findSource(sourceName)
        contents = source.getContentList()
        for i in xrange(len(contents)):
            self.sourceContentList.addItem(QListWidgetItem(contents[i][0]))


    def findSource(self, sourceName):
        test = source.Source("Iraq", 'C:\Users\OmarAli\Google Drive\Research\SimpleResearch\simple-research\Iraq')
        return test





