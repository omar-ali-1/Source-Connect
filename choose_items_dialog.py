# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_items_dialog.ui'
#
# Created: Fri Nov 04 17:07:22 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_chooseContentDialog(object):
    def setupUi(self, chooseContentDialog):
        chooseContentDialog.setObjectName("chooseContentDialog")
        chooseContentDialog.resize(608, 694)
        self.buttonBox = QtGui.QDialogButtonBox(chooseContentDialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 640, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.chooseItemDialogList = QtGui.QListWidget(chooseContentDialog)
        self.chooseItemDialogList.setGeometry(QtCore.QRect(30, 80, 551, 541))
        self.chooseItemDialogList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.chooseItemDialogList.setObjectName("chooseItemDialogList")
        self.label = QtGui.QLabel(chooseContentDialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.chooseItemDialogLineEdit = QtGui.QLineEdit(chooseContentDialog)
        self.chooseItemDialogLineEdit.setGeometry(QtCore.QRect(30, 50, 471, 20))
        self.chooseItemDialogLineEdit.setObjectName("chooseItemDialogLineEdit")
        self.chooseItemsSearchButton = QtGui.QPushButton(chooseContentDialog)
        self.chooseItemsSearchButton.setGeometry(QtCore.QRect(510, 50, 75, 23))
        self.chooseItemsSearchButton.setObjectName("chooseItemsSearchButton")

        self.retranslateUi(chooseContentDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), chooseContentDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), chooseContentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(chooseContentDialog)

    def retranslateUi(self, chooseContentDialog):
        chooseContentDialog.setWindowTitle(QtGui.QApplication.translate("chooseContentDialog", "Choose Items", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("chooseContentDialog", "Select Items to Add", None, QtGui.QApplication.UnicodeUTF8))
        self.chooseItemsSearchButton.setText(QtGui.QApplication.translate("chooseContentDialog", "Search", None, QtGui.QApplication.UnicodeUTF8))

