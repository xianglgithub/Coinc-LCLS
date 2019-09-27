# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XY1GatedTof.ui'
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

class Ui_XY1GatedTof(object):
    def setupUi(self, XY1GatedTof):
        XY1GatedTof.setObjectName(_fromUtf8("XY1GatedTof"))
        XY1GatedTof.resize(800, 600)
        self.centralwidget = QtGui.QWidget(XY1GatedTof)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        XY1GatedTof.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(XY1GatedTof)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        XY1GatedTof.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(XY1GatedTof)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        XY1GatedTof.setStatusBar(self.statusbar)

        self.retranslateUi(XY1GatedTof)
        QtCore.QMetaObject.connectSlotsByName(XY1GatedTof)

    def retranslateUi(self, XY1GatedTof):
        XY1GatedTof.setWindowTitle(_translate("XY1GatedTof", "XY1GatedTof", None))

