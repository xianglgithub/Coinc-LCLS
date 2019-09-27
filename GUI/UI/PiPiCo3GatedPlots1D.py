# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PiPiCo3GatedPlots1D.ui'
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

class Ui_PiPiCo3GatedPlots1D(object):
    def setupUi(self, PiPiCo3GatedPlots1D):
        PiPiCo3GatedPlots1D.setObjectName(_fromUtf8("PiPiCo3GatedPlots1D"))
        PiPiCo3GatedPlots1D.resize(800, 600)
        self.centralwidget = QtGui.QWidget(PiPiCo3GatedPlots1D)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        PiPiCo3GatedPlots1D.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PiPiCo3GatedPlots1D)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PiPiCo3GatedPlots1D.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PiPiCo3GatedPlots1D)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PiPiCo3GatedPlots1D.setStatusBar(self.statusbar)

        self.retranslateUi(PiPiCo3GatedPlots1D)
        QtCore.QMetaObject.connectSlotsByName(PiPiCo3GatedPlots1D)

    def retranslateUi(self, PiPiCo3GatedPlots1D):
        PiPiCo3GatedPlots1D.setWindowTitle(_translate("PiPiCo3GatedPlots1D", "PiPiCo3GatedPlots1D", None))

