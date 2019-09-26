# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ControlPanel(object):
    def setupUi(self, ControlPanel):
        ControlPanel.setObjectName(_fromUtf8("ControlPanel"))
        ControlPanel.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ControlPanel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Clear = QtGui.QPushButton(ControlPanel)
        self.Clear.setObjectName(_fromUtf8("Clear"))
        self.verticalLayout.addWidget(self.Clear)
        self.SaveandClear = QtGui.QPushButton(ControlPanel)
        self.SaveandClear.setObjectName(_fromUtf8("SaveandClear"))
        self.verticalLayout.addWidget(self.SaveandClear)

        self.retranslateUi(ControlPanel)
        QtCore.QMetaObject.connectSlotsByName(ControlPanel)

    def retranslateUi(self, ControlPanel):
        ControlPanel.setWindowTitle(_translate("ControlPanel", "Control Panel", None))
        self.Clear.setText(_translate("ControlPanel", "Clear", None))
        self.SaveandClear.setText(_translate("ControlPanel", "Save and Clear", None))

