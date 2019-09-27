# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tof1GatedPlots1D.ui'
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

class Ui_Tof1GatePlots1D(object):
    def setupUi(self, Tof1GatePlots1D):
        Tof1GatePlots1D.setObjectName(_fromUtf8("Tof1GatePlots1D"))
        Tof1GatePlots1D.resize(800, 600)
        self.centralwidget = QtGui.QWidget(Tof1GatePlots1D)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        Tof1GatePlots1D.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Tof1GatePlots1D)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Tof1GatePlots1D.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Tof1GatePlots1D)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Tof1GatePlots1D.setStatusBar(self.statusbar)

        self.retranslateUi(Tof1GatePlots1D)
        QtCore.QMetaObject.connectSlotsByName(Tof1GatePlots1D)

    def retranslateUi(self, Tof1GatePlots1D):
        Tof1GatePlots1D.setWindowTitle(_translate("Tof1GatePlots1D", "Tof1GatedPlots1D", None))

