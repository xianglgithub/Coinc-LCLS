# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_eXY_push.ui'
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

class Ui_eXY(object):
    def setupUi(self, eXY):
        eXY.setObjectName(_fromUtf8("eXY"))
        eXY.resize(800, 600)
        self.centralwidget = QtGui.QWidget(eXY)
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
        self.ARG3 = QtGui.QPushButton(self.centralwidget)
        self.ARG3.setObjectName(_fromUtf8("ARG3"))
        self.horizontalLayout.addWidget(self.ARG3)
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
        self.RRG3 = QtGui.QPushButton(self.centralwidget)
        self.RRG3.setObjectName(_fromUtf8("RRG3"))
        self.horizontalLayout_4.addWidget(self.RRG3)
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
        self.Rect3Yield = QtGui.QLabel(self.centralwidget)
        self.Rect3Yield.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.Rect3Yield.setObjectName(_fromUtf8("Rect3Yield"))
        self.horizontalLayout_2.addWidget(self.Rect3Yield)
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
        self.Rect3Rate = QtGui.QLabel(self.centralwidget)
        self.Rect3Rate.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.Rect3Rate.setObjectName(_fromUtf8("Rect3Rate"))
        self.horizontalLayout_3.addWidget(self.Rect3Rate)
        self.TotalRate = QtGui.QLabel(self.centralwidget)
        self.TotalRate.setObjectName(_fromUtf8("TotalRate"))
        self.horizontalLayout_3.addWidget(self.TotalRate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        eXY.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(eXY)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        eXY.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(eXY)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        eXY.setStatusBar(self.statusbar)

        self.retranslateUi(eXY)
        QtCore.QMetaObject.connectSlotsByName(eXY)

    def retranslateUi(self, eXY):
        eXY.setWindowTitle(_translate("eXY", "eXY", None))
        self.ARG1.setText(_translate("eXY", "Add RectGate1", None))
        self.ARG2.setText(_translate("eXY", "Add RectGate2", None))
        self.ARG3.setText(_translate("eXY", "Add RectGate3", None))
        self.MousePosition.setText(_translate("eXY", "MousePosition", None))
        self.RRG1.setText(_translate("eXY", "Remove RectGate1", None))
        self.RRG2.setText(_translate("eXY", "Remove RectGate2", None))
        self.RRG3.setText(_translate("eXY", "Remove RectGate3", None))
        self.AndGate.setText(_translate("eXY", "AndGate", None))
        self.Rect1Yield.setText(_translate("eXY", "Rect1Yield", None))
        self.Rect2Yield.setText(_translate("eXY", "Rect2Yield", None))
        self.Rect3Yield.setText(_translate("eXY", "Rect3Yield", None))
        self.TotalYield.setText(_translate("eXY", "TotalYield", None))
        self.Rect1Rate.setText(_translate("eXY", "Rect1Rate", None))
        self.Rect2Rate.setText(_translate("eXY", "Rect2Rate", None))
        self.Rect3Rate.setText(_translate("eXY", "Rect3Rate", None))
        self.TotalRate.setText(_translate("eXY", "TotalRate", None))

