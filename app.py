import sys
from PySide.QtCore import *
from PySide.QtGui import *
import MainWindow
import Source

class MainWindow(QMainWindow, MainWindow.Ui_sourceConnectMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
        test = Source.Source("Iraq", 'C:\Users\OmarAli\Google Drive\Research\SimpleResearch\simple-research\Iraq')
        return test





app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()