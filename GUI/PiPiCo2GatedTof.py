# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PiPiCo2GatedTof.ui'
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

class Ui_PiPiCo2GatedTof(object):
    def setupUi(self, PiPiCo2GatedTof):
        PiPiCo2GatedTof.setObjectName(_fromUtf8("PiPiCo2GatedTof"))
        PiPiCo2GatedTof.resize(800, 600)
        self.centralwidget = QtGui.QWidget(PiPiCo2GatedTof)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        PiPiCo2GatedTof.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PiPiCo2GatedTof)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PiPiCo2GatedTof.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PiPiCo2GatedTof)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PiPiCo2GatedTof.setStatusBar(self.statusbar)

        self.retranslateUi(PiPiCo2GatedTof)
        QtCore.QMetaObject.connectSlotsByName(PiPiCo2GatedTof)

    def retranslateUi(self, PiPiCo2GatedTof):
        PiPiCo2GatedTof.setWindowTitle(_translate("PiPiCo2GatedTof", "PiPiCo2GatedTof", None))

