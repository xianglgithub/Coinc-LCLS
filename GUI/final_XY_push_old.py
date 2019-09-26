# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_XY_push_old.ui'
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

class Ui_XY(object):
    def setupUi(self, XY):
        XY.setObjectName(_fromUtf8("XY"))
        XY.resize(800, 600)
        self.centralwidget = QtGui.QWidget(XY)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ARG1 = QtGui.QPushButton(self.centralwidget)
        self.ARG1.setObjectName(_fromUtf8("ARG1"))
        self.horizontalLayout.addWidget(self.ARG1)
        self.ARG2 = QtGui.QPushButton(self.centralwidget)
        self.ARG2.setObjectName(_fromUtf8("ARG2"))
        self.horizontalLayout.addWidget(self.ARG2)
        self.ACG = QtGui.QPushButton(self.centralwidget)
        self.ACG.setObjectName(_fromUtf8("ACG"))
        self.horizontalLayout.addWidget(self.ACG)
        self.MousePosition = QtGui.QLabel(self.centralwidget)
        self.MousePosition.setObjectName(_fromUtf8("MousePosition"))
        self.horizontalLayout.addWidget(self.MousePosition)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.RRG1 = QtGui.QPushButton(self.centralwidget)
        self.RRG1.setObjectName(_fromUtf8("RRG1"))
        self.horizontalLayout_4.addWidget(self.RRG1)
        self.RRG2 = QtGui.QPushButton(self.centralwidget)
        self.RRG2.setObjectName(_fromUtf8("RRG2"))
        self.horizontalLayout_4.addWidget(self.RRG2)
        self.RCG = QtGui.QPushButton(self.centralwidget)
        self.RCG.setObjectName(_fromUtf8("RCG"))
        self.horizontalLayout_4.addWidget(self.RCG)
        self.AndGate = QtGui.QCheckBox(self.centralwidget)
        self.AndGate.setObjectName(_fromUtf8("AndGate"))
        self.horizontalLayout_4.addWidget(self.AndGate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Rect1Yield = QtGui.QLabel(self.centralwidget)
        self.Rect1Yield.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.Rect1Yield.setObjectName(_fromUtf8("Rect1Yield"))
        self.horizontalLayout_2.addWidget(self.Rect1Yield)
        self.Rect2Yield = QtGui.QLabel(self.centralwidget)
        self.Rect2Yield.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Rect2Yield.setObjectName(_fromUtf8("Rect2Yield"))
        self.horizontalLayout_2.addWidget(self.Rect2Yield)
        self.CircleYield = QtGui.QLabel(self.centralwidget)
        self.CircleYield.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.CircleYield.setObjectName(_fromUtf8("CircleYield"))
        self.horizontalLayout_2.addWidget(self.CircleYield)
        self.TotalYield = QtGui.QLabel(self.centralwidget)
        self.TotalYield.setObjectName(_fromUtf8("TotalYield"))
        self.horizontalLayout_2.addWidget(self.TotalYield)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.Rect1Rate = QtGui.QLabel(self.centralwidget)
        self.Rect1Rate.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.Rect1Rate.setObjectName(_fromUtf8("Rect1Rate"))
        self.horizontalLayout_3.addWidget(self.Rect1Rate)
        self.Rect2Rate = QtGui.QLabel(self.centralwidget)
        self.Rect2Rate.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Rect2Rate.setObjectName(_fromUtf8("Rect2Rate"))
        self.horizontalLayout_3.addWidget(self.Rect2Rate)
        self.CircleRate = QtGui.QLabel(self.centralwidget)
        self.CircleRate.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.CircleRate.setObjectName(_fromUtf8("CircleRate"))
        self.horizontalLayout_3.addWidget(self.CircleRate)
        self.TotalRate = QtGui.QLabel(self.centralwidget)
        self.TotalRate.setObjectName(_fromUtf8("TotalRate"))
        self.horizontalLayout_3.addWidget(self.TotalRate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        XY.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(XY)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        XY.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(XY)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        XY.setStatusBar(self.statusbar)

        self.retranslateUi(XY)
        QtCore.QMetaObject.connectSlotsByName(XY)

    def retranslateUi(self, XY):
        XY.setWindowTitle(_translate("XY", "XY", None))
        self.ARG1.setText(_translate("XY", "Add RectGate1", None))
        self.ARG2.setText(_translate("XY", "Add RectGate2", None))
        self.ACG.setText(_translate("XY", "Add CircleGate", None))
        self.MousePosition.setText(_translate("XY", "MousePosition", None))
        self.RRG1.setText(_translate("XY", "Remove RectGate1", None))
        self.RRG2.setText(_translate("XY", "Remove RectGate2", None))
        self.RCG.setText(_translate("XY", "Remove CircleGate", None))
        self.AndGate.setText(_translate("XY", "AndGate", None))
        self.Rect1Yield.setText(_translate("XY", "Rect1Yield", None))
        self.Rect2Yield.setText(_translate("XY", "Rect2Yield", None))
        self.CircleYield.setText(_translate("XY", "CircleYield", None))
        self.TotalYield.setText(_translate("XY", "TotalYield", None))
        self.Rect1Rate.setText(_translate("XY", "Rect1Rate", None))
        self.Rect2Rate.setText(_translate("XY", "Rect2Rate", None))
        self.CircleRate.setText(_translate("XY", "CircleRate", None))
        self.TotalRate.setText(_translate("XY", "TotalRate", None))

