# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eXY2GatedTof.ui'
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

class Ui_eXY2GatedTof(object):
    def setupUi(self, eXY2GatedTof):
        eXY2GatedTof.setObjectName(_fromUtf8("eXY2GatedTof"))
        eXY2GatedTof.resize(800, 600)
        self.centralwidget = QtGui.QWidget(eXY2GatedTof)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        eXY2GatedTof.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(eXY2GatedTof)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        eXY2GatedTof.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(eXY2GatedTof)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        eXY2GatedTof.setStatusBar(self.statusbar)

        self.retranslateUi(eXY2GatedTof)
        QtCore.QMetaObject.connectSlotsByName(eXY2GatedTof)

    def retranslateUi(self, eXY2GatedTof):
        eXY2GatedTof.setWindowTitle(_translate("eXY2GatedTof", "eXY2GatedTof", None))

