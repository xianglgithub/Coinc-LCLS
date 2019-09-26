# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_Tof.ui'
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

class Ui_Tof(object):
    def setupUi(self, Tof):
        Tof.setObjectName(_fromUtf8("Tof"))
        Tof.resize(800, 600)
        self.centralwidget = QtGui.QWidget(Tof)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Gate1 = QtGui.QCheckBox(self.centralwidget)
        self.Gate1.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.Gate1.setObjectName(_fromUtf8("Gate1"))
        self.horizontalLayout.addWidget(self.Gate1)
        self.Gate2 = QtGui.QCheckBox(self.centralwidget)
        self.Gate2.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Gate2.setObjectName(_fromUtf8("Gate2"))
        self.horizontalLayout.addWidget(self.Gate2)
        self.Gate3 = QtGui.QCheckBox(self.centralwidget)
        self.Gate3.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255);"))
        self.Gate3.setObjectName(_fromUtf8("Gate3"))
        self.horizontalLayout.addWidget(self.Gate3)
        self.MousePosition = QtGui.QLabel(self.centralwidget)
        self.MousePosition.setObjectName(_fromUtf8("MousePosition"))
        self.horizontalLayout.addWidget(self.MousePosition)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Gate1Yield = QtGui.QLabel(self.centralwidget)
        self.Gate1Yield.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.Gate1Yield.setObjectName(_fromUtf8("Gate1Yield"))
        self.horizontalLayout_2.addWidget(self.Gate1Yield)
        self.Gate2Yield = QtGui.QLabel(self.centralwidget)
        self.Gate2Yield.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Gate2Yield.setObjectName(_fromUtf8("Gate2Yield"))
        self.horizontalLayout_2.addWidget(self.Gate2Yield)
        self.Gate3Yield = QtGui.QLabel(self.centralwidget)
        self.Gate3Yield.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255);"))
        self.Gate3Yield.setObjectName(_fromUtf8("Gate3Yield"))
        self.horizontalLayout_2.addWidget(self.Gate3Yield)
        self.TotalYield = QtGui.QLabel(self.centralwidget)
        self.TotalYield.setObjectName(_fromUtf8("TotalYield"))
        self.horizontalLayout_2.addWidget(self.TotalYield)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.Gate1Rate = QtGui.QLabel(self.centralwidget)
        self.Gate1Rate.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.Gate1Rate.setObjectName(_fromUtf8("Gate1Rate"))
        self.horizontalLayout_3.addWidget(self.Gate1Rate)
        self.Gate2Rate = QtGui.QLabel(self.centralwidget)
        self.Gate2Rate.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Gate2Rate.setObjectName(_fromUtf8("Gate2Rate"))
        self.horizontalLayout_3.addWidget(self.Gate2Rate)
        self.Gate3Rate = QtGui.QLabel(self.centralwidget)
        self.Gate3Rate.setStyleSheet(_fromUtf8("color: rgb(0, 0, 255);"))
        self.Gate3Rate.setObjectName(_fromUtf8("Gate3Rate"))
        self.horizontalLayout_3.addWidget(self.Gate3Rate)
        self.TotalRate = QtGui.QLabel(self.centralwidget)
        self.TotalRate.setObjectName(_fromUtf8("TotalRate"))
        self.horizontalLayout_3.addWidget(self.TotalRate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        Tof.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Tof)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Tof.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Tof)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Tof.setStatusBar(self.statusbar)

        self.retranslateUi(Tof)
        QtCore.QMetaObject.connectSlotsByName(Tof)

    def retranslateUi(self, Tof):
        Tof.setWindowTitle(_translate("Tof", "Tof", None))
        self.Gate1.setText(_translate("Tof", "Gate1", None))
        self.Gate2.setText(_translate("Tof", "Gate2", None))
        self.Gate3.setText(_translate("Tof", "Gate3", None))
        self.MousePosition.setText(_translate("Tof", "MousePosition", None))
        self.Gate1Yield.setText(_translate("Tof", "Gate1Yield", None))
        self.Gate2Yield.setText(_translate("Tof", "Gate2Yield", None))
        self.Gate3Yield.setText(_translate("Tof", "Gate3Yield", None))
        self.TotalYield.setText(_translate("Tof", "TotalYield", None))
        self.Gate1Rate.setText(_translate("Tof", "Gate1Rate", None))
        self.Gate2Rate.setText(_translate("Tof", "Gate2Rate", None))
        self.Gate3Rate.setText(_translate("Tof", "Gate3Rate", None))
        self.TotalRate.setText(_translate("Tof", "TotalRate", None))

