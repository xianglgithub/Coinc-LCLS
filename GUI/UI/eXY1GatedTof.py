# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eXY1GatedTof.ui'
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

class Ui_eXY1GatedTof(object):
    def setupUi(self, eXY1GatedTof):
        eXY1GatedTof.setObjectName(_fromUtf8("eXY1GatedTof"))
        eXY1GatedTof.resize(800, 600)
        self.centralwidget = QtGui.QWidget(eXY1GatedTof)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        eXY1GatedTof.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(eXY1GatedTof)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        eXY1GatedTof.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(eXY1GatedTof)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        eXY1GatedTof.setStatusBar(self.statusbar)

        self.retranslateUi(eXY1GatedTof)
        QtCore.QMetaObject.connectSlotsByName(eXY1GatedTof)

    def retranslateUi(self, eXY1GatedTof):
        eXY1GatedTof.setWindowTitle(_translate("eXY1GatedTof", "eXY1GatedTof", None))

