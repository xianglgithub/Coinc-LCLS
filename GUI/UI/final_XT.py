# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_XT.ui'
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

class Ui_XT(object):
    def setupUi(self, XT):
        XT.setObjectName(_fromUtf8("XT"))
        XT.resize(800, 600)
        self.centralwidget = QtGui.QWidget(XT)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.RectGate = QtGui.QCheckBox(self.centralwidget)
        self.RectGate.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.RectGate.setObjectName(_fromUtf8("RectGate"))
        self.horizontalLayout.addWidget(self.RectGate)
        self.CircleGate1 = QtGui.QCheckBox(self.centralwidget)
        self.CircleGate1.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.CircleGate1.setObjectName(_fromUtf8("CircleGate1"))
        self.horizontalLayout.addWidget(self.CircleGate1)
        self.CircleGate2 = QtGui.QCheckBox(self.centralwidget)
        self.CircleGate2.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.CircleGate2.setObjectName(_fromUtf8("CircleGate2"))
        self.horizontalLayout.addWidget(self.CircleGate2)
        self.MousePosition = QtGui.QLabel(self.centralwidget)
        self.MousePosition.setObjectName(_fromUtf8("MousePosition"))
        self.horizontalLayout.addWidget(self.MousePosition)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.RectYield = QtGui.QLabel(self.centralwidget)
        self.RectYield.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.RectYield.setObjectName(_fromUtf8("RectYield"))
        self.horizontalLayout_2.addWidget(self.RectYield)
        self.Circle1Yield = QtGui.QLabel(self.centralwidget)
        self.Circle1Yield.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Circle1Yield.setObjectName(_fromUtf8("Circle1Yield"))
        self.horizontalLayout_2.addWidget(self.Circle1Yield)
        self.Circle2Yield = QtGui.QLabel(self.centralwidget)
        self.Circle2Yield.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.Circle2Yield.setObjectName(_fromUtf8("Circle2Yield"))
        self.horizontalLayout_2.addWidget(self.Circle2Yield)
        self.TotalYield = QtGui.QLabel(self.centralwidget)
        self.TotalYield.setObjectName(_fromUtf8("TotalYield"))
        self.horizontalLayout_2.addWidget(self.TotalYield)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.RectRate = QtGui.QLabel(self.centralwidget)
        self.RectRate.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.RectRate.setObjectName(_fromUtf8("RectRate"))
        self.horizontalLayout_3.addWidget(self.RectRate)
        self.Circle1Rate = QtGui.QLabel(self.centralwidget)
        self.Circle1Rate.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.Circle1Rate.setObjectName(_fromUtf8("Circle1Rate"))
        self.horizontalLayout_3.addWidget(self.Circle1Rate)
        self.Circle2Rate = QtGui.QLabel(self.centralwidget)
        self.Circle2Rate.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);"))
        self.Circle2Rate.setObjectName(_fromUtf8("Circle2Rate"))
        self.horizontalLayout_3.addWidget(self.Circle2Rate)
        self.TotalRate = QtGui.QLabel(self.centralwidget)
        self.TotalRate.setObjectName(_fromUtf8("TotalRate"))
        self.horizontalLayout_3.addWidget(self.TotalRate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        XT.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(XT)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        XT.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(XT)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        XT.setStatusBar(self.statusbar)

        self.retranslateUi(XT)
        QtCore.QMetaObject.connectSlotsByName(XT)

    def retranslateUi(self, XT):
        XT.setWindowTitle(_translate("XT", "XT", None))
        self.RectGate.setText(_translate("XT", "RectGate", None))
        self.CircleGate1.setText(_translate("XT", "CircleGate1", None))
        self.CircleGate2.setText(_translate("XT", "CircleGate2", None))
        self.MousePosition.setText(_translate("XT", "MousePosition", None))
        self.RectYield.setText(_translate("XT", "RectYield", None))
        self.Circle1Yield.setText(_translate("XT", "Circle1Yield", None))
        self.Circle2Yield.setText(_translate("XT", "Circle2Yield", None))
        self.TotalYield.setText(_translate("XT", "TotalYield", None))
        self.RectRate.setText(_translate("XT", "RectRate", None))
        self.Circle1Rate.setText(_translate("XT", "Circle1Rate", None))
        self.Circle2Rate.setText(_translate("XT", "Circle2Rate", None))
        self.TotalRate.setText(_translate("XT", "TotalRate", None))

