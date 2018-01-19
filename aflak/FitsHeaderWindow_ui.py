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
        FitsHeaderWindow.resize(1350, 900)
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
        self.fileNameField = QtWidgets.QLineEdit(FitsHeaderWindow)
        self.fileNameField.setReadOnly(True)
        self.fileNameField.setObjectName("fileNameField")
        self.gridLayout.addWidget(self.fileNameField, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(FitsHeaderWindow)
        self.tabWidget.setObjectName("tabWidget")
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
        FitsHeaderWindow.setWindowTitle(_translate("FitsHeaderWindow", "FITS header info"))
        self.label.setText(_translate("FitsHeaderWindow", "FITS file name"))
        self.closeButton.setText(_translate("FitsHeaderWindow", "Close"))

