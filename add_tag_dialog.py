# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_tag_dialog.ui'
#
# Created: Fri Nov 04 16:08:37 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AddTagDialog(object):
    def setupUi(self, AddTagDialog):
        AddTagDialog.setObjectName("AddTagDialog")
        AddTagDialog.resize(400, 125)
        self.gridLayout = QtGui.QGridLayout(AddTagDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.addTagLineEdit = QtGui.QLineEdit(AddTagDialog)
        self.addTagLineEdit.setObjectName("addTagLineEdit")
        self.gridLayout.addWidget(self.addTagLineEdit, 1, 0, 1, 1)
        self.addTagButtons = QtGui.QDialogButtonBox(AddTagDialog)
        self.addTagButtons.setOrientation(QtCore.Qt.Horizontal)
        self.addTagButtons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.addTagButtons.setObjectName("addTagButtons")
        self.gridLayout.addWidget(self.addTagButtons, 2, 0, 1, 1)
        self.tagNameLable = QtGui.QLabel(AddTagDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.tagNameLable.setFont(font)
        self.tagNameLable.setTextFormat(QtCore.Qt.RichText)
        self.tagNameLable.setObjectName("tagNameLable")
        self.gridLayout.addWidget(self.tagNameLable, 0, 0, 1, 1)

        self.retranslateUi(AddTagDialog)
        QtCore.QObject.connect(self.addTagButtons, QtCore.SIGNAL("accepted()"), AddTagDialog.accept)
        QtCore.QObject.connect(self.addTagButtons, QtCore.SIGNAL("rejected()"), AddTagDialog.reject)
        QtCore.QObject.connect(self.addTagLineEdit, QtCore.SIGNAL("returnPressed()"), AddTagDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AddTagDialog)
        AddTagDialog.setTabOrder(self.addTagLineEdit, self.addTagButtons)

    def retranslateUi(self, AddTagDialog):
        AddTagDialog.setWindowTitle(QtGui.QApplication.translate("AddTagDialog", "Add Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.addTagLineEdit.setToolTip(QtGui.QApplication.translate("AddTagDialog", "Type new tag name here and press OK to save or Cancel to discard.", None, QtGui.QApplication.UnicodeUTF8))
        self.addTagLineEdit.setPlaceholderText(QtGui.QApplication.translate("AddTagDialog", "Type new tag name here and press OK to save or Cancel to discard.", None, QtGui.QApplication.UnicodeUTF8))
        self.tagNameLable.setText(QtGui.QApplication.translate("AddTagDialog", "Tag Name", None, QtGui.QApplication.UnicodeUTF8))

