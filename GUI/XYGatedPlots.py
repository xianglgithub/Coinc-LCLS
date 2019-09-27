# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XYGatedPlots.ui'
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

class Ui_XYGatedPlots(object):
    def setupUi(self, XYGatedPlots):
        XYGatedPlots.setObjectName(_fromUtf8("XYGatedPlots"))
        XYGatedPlots.resize(800, 600)
        self.centralwidget = QtGui.QWidget(XYGatedPlots)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.RectGate1_HL = QtGui.QHBoxLayout()
        self.RectGate1_HL.setObjectName(_fromUtf8("RectGate1_HL"))
        self.RectGate1_VL = QtGui.QVBoxLayout()
        self.RectGate1_VL.setObjectName(_fromUtf8("RectGate1_VL"))
        self.RectGate1 = QtGui.QLabel(self.centralwidget)
        self.RectGate1.setObjectName(_fromUtf8("RectGate1"))
        self.RectGate1_VL.addWidget(self.RectGate1)
        self.RG1V1 = QtGui.QVBoxLayout()
        self.RG1V1.setObjectName(_fromUtf8("RG1V1"))
        self.RectGate1_VL.addLayout(self.RG1V1)
        self.RG1V2 = QtGui.QVBoxLayout()
        self.RG1V2.setObjectName(_fromUtf8("RG1V2"))
        self.RectGate1_VL.addLayout(self.RG1V2)
        self.RG1V3 = QtGui.QVBoxLayout()
        self.RG1V3.setObjectName(_fromUtf8("RG1V3"))
        self.RectGate1_VL.addLayout(self.RG1V3)
        self.RG1V4 = QtGui.QVBoxLayout()
        self.RG1V4.setObjectName(_fromUtf8("RG1V4"))
        self.RectGate1_VL.addLayout(self.RG1V4)
        self.RG1V5 = QtGui.QVBoxLayout()
        self.RG1V5.setObjectName(_fromUtf8("RG1V5"))
        self.RectGate1_VL.addLayout(self.RG1V5)
        self.RG1V6 = QtGui.QVBoxLayout()
        self.RG1V6.setObjectName(_fromUtf8("RG1V6"))
        self.RectGate1_VL.addLayout(self.RG1V6)
        self.RectGate1_HL.addLayout(self.RectGate1_VL)
        self.horizontalLayout.addLayout(self.RectGate1_HL)
        self.RectGate2_HL = QtGui.QHBoxLayout()
        self.RectGate2_HL.setObjectName(_fromUtf8("RectGate2_HL"))
        self.RectGate2_VL = QtGui.QVBoxLayout()
        self.RectGate2_VL.setObjectName(_fromUtf8("RectGate2_VL"))
        self.RectGate2 = QtGui.QLabel(self.centralwidget)
        self.RectGate2.setObjectName(_fromUtf8("RectGate2"))
        self.RectGate2_VL.addWidget(self.RectGate2)
        self.RG2V1 = QtGui.QVBoxLayout()
        self.RG2V1.setObjectName(_fromUtf8("RG2V1"))
        self.RectGate2_VL.addLayout(self.RG2V1)
        self.RG2V2 = QtGui.QVBoxLayout()
        self.RG2V2.setObjectName(_fromUtf8("RG2V2"))
        self.RectGate2_VL.addLayout(self.RG2V2)
        self.RG2V3 = QtGui.QVBoxLayout()
        self.RG2V3.setObjectName(_fromUtf8("RG2V3"))
        self.RectGate2_VL.addLayout(self.RG2V3)
        self.RG2V4 = QtGui.QVBoxLayout()
        self.RG2V4.setObjectName(_fromUtf8("RG2V4"))
        self.RectGate2_VL.addLayout(self.RG2V4)
        self.RG2V5 = QtGui.QVBoxLayout()
        self.RG2V5.setObjectName(_fromUtf8("RG2V5"))
        self.RectGate2_VL.addLayout(self.RG2V5)
        self.RG2V6 = QtGui.QVBoxLayout()
        self.RG2V6.setObjectName(_fromUtf8("RG2V6"))
        self.RectGate2_VL.addLayout(self.RG2V6)
        self.RectGate2_HL.addLayout(self.RectGate2_VL)
        self.horizontalLayout.addLayout(self.RectGate2_HL)
        self.CicleGate1_HL = QtGui.QHBoxLayout()
        self.CicleGate1_HL.setObjectName(_fromUtf8("CicleGate1_HL"))
        self.CircleGate1_VL = QtGui.QVBoxLayout()
        self.CircleGate1_VL.setObjectName(_fromUtf8("CircleGate1_VL"))
        self.CircleGate = QtGui.QLabel(self.centralwidget)
        self.CircleGate.setObjectName(_fromUtf8("CircleGate"))
        self.CircleGate1_VL.addWidget(self.CircleGate)
        self.CGV1 = QtGui.QVBoxLayout()
        self.CGV1.setObjectName(_fromUtf8("CGV1"))
        self.CircleGate1_VL.addLayout(self.CGV1)
        self.CGV2 = QtGui.QVBoxLayout()
        self.CGV2.setObjectName(_fromUtf8("CGV2"))
        self.CircleGate1_VL.addLayout(self.CGV2)
        self.CGV3 = QtGui.QVBoxLayout()
        self.CGV3.setObjectName(_fromUtf8("CGV3"))
        self.CircleGate1_VL.addLayout(self.CGV3)
        self.CGV4 = QtGui.QVBoxLayout()
        self.CGV4.setObjectName(_fromUtf8("CGV4"))
        self.CircleGate1_VL.addLayout(self.CGV4)
        self.CGV5 = QtGui.QVBoxLayout()
        self.CGV5.setObjectName(_fromUtf8("CGV5"))
        self.CircleGate1_VL.addLayout(self.CGV5)
        self.CGV6 = QtGui.QVBoxLayout()
        self.CGV6.setObjectName(_fromUtf8("CGV6"))
        self.CircleGate1_VL.addLayout(self.CGV6)
        self.CicleGate1_HL.addLayout(self.CircleGate1_VL)
        self.horizontalLayout.addLayout(self.CicleGate1_HL)
        XYGatedPlots.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(XYGatedPlots)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        XYGatedPlots.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(XYGatedPlots)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        XYGatedPlots.setStatusBar(self.statusbar)

        self.retranslateUi(XYGatedPlots)
        QtCore.QMetaObject.connectSlotsByName(XYGatedPlots)

    def retranslateUi(self, XYGatedPlots):
        XYGatedPlots.setWindowTitle(_translate("XYGatedPlots", "XYGatedPlots", None))
        self.RectGate1.setText(_translate("XYGatedPlots", "RectGate1", None))
        self.RectGate2.setText(_translate("XYGatedPlots", "RectGate2", None))
        self.CircleGate.setText(_translate("XYGatedPlots", "CircleGate", None))

