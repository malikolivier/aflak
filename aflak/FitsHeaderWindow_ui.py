# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aflak/FitsHeaderWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FitsHeaderWindow(object):
    def setupUi(self, FitsHeaderWindow):
        FitsHeaderWindow.setObjectName("FitsHeaderWindow")
        FitsHeaderWindow.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FitsHeaderWindow.sizePolicy().hasHeightForWidth())
        FitsHeaderWindow.setSizePolicy(sizePolicy)
        FitsHeaderWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtWidgets.QGridLayout(FitsHeaderWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(FitsHeaderWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(FitsHeaderWindow)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(FitsHeaderWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_2.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 2)
        self.closeButton = QtWidgets.QPushButton(FitsHeaderWindow)
        self.closeButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.closeButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 2, 0, 1, 1)

        self.retranslateUi(FitsHeaderWindow)
        QtCore.QMetaObject.connectSlotsByName(FitsHeaderWindow)

    def retranslateUi(self, FitsHeaderWindow):
        _translate = QtCore.QCoreApplication.translate
        FitsHeaderWindow.setWindowTitle(_translate("FitsHeaderWindow", "Dialog"))
        self.label.setText(_translate("FitsHeaderWindow", "FITS file name"))
        self.plainTextEdit.setPlainText(_translate("FitsHeaderWindow", "test"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("FitsHeaderWindow", "[0] Primary"))
        self.closeButton.setText(_translate("FitsHeaderWindow", "Close"))