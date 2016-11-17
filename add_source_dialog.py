# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_source_dialog.ui'
#
# Created: Wed Nov 09 16:50:01 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AddSourceDialog(object):
    def setupUi(self, AddSourceDialog):
        AddSourceDialog.setObjectName("AddSourceDialog")
        AddSourceDialog.resize(400, 125)
        self.gridLayout = QtGui.QGridLayout(AddSourceDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.addSourceLineEdit = QtGui.QLineEdit(AddSourceDialog)
        self.addSourceLineEdit.setObjectName("addSourceLineEdit")
        self.gridLayout.addWidget(self.addSourceLineEdit, 1, 0, 1, 1)
        self.addSourceButtons = QtGui.QDialogButtonBox(AddSourceDialog)
        self.addSourceButtons.setOrientation(QtCore.Qt.Horizontal)
        self.addSourceButtons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.addSourceButtons.setObjectName("addSourceButtons")
        self.gridLayout.addWidget(self.addSourceButtons, 2, 0, 1, 1)
        self.sourceNameLable = QtGui.QLabel(AddSourceDialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.sourceNameLable.setFont(font)
        self.sourceNameLable.setTextFormat(QtCore.Qt.RichText)
        self.sourceNameLable.setObjectName("sourceNameLable")
        self.gridLayout.addWidget(self.sourceNameLable, 0, 0, 1, 1)

        self.retranslateUi(AddSourceDialog)
        QtCore.QObject.connect(self.addSourceButtons, QtCore.SIGNAL("accepted()"), AddSourceDialog.accept)
        QtCore.QObject.connect(self.addSourceButtons, QtCore.SIGNAL("rejected()"), AddSourceDialog.reject)
        QtCore.QObject.connect(self.addSourceLineEdit, QtCore.SIGNAL("returnPressed()"), AddSourceDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AddSourceDialog)
        AddSourceDialog.setTabOrder(self.addSourceLineEdit, self.addSourceButtons)

    def retranslateUi(self, AddSourceDialog):
        AddSourceDialog.setWindowTitle(QtGui.QApplication.translate("AddSourceDialog", "Add Source", None, QtGui.QApplication.UnicodeUTF8))
        self.addSourceLineEdit.setToolTip(QtGui.QApplication.translate("AddSourceDialog", "Type new source name here and press OK to save or Cancel to discard.", None, QtGui.QApplication.UnicodeUTF8))
        self.addSourceLineEdit.setPlaceholderText(QtGui.QApplication.translate("AddSourceDialog", "Type new source name here and press OK to save or Cancel to discard.", None, QtGui.QApplication.UnicodeUTF8))
        self.sourceNameLable.setText(QtGui.QApplication.translate("AddSourceDialog", "Source Name", None, QtGui.QApplication.UnicodeUTF8))

