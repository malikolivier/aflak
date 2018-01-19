# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aflak/AboutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(759, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        AboutDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtWidgets.QGridLayout(AboutDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.aflakName = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.aflakName.setFont(font)
        self.aflakName.setAlignment(QtCore.Qt.AlignCenter)
        self.aflakName.setWordWrap(True)
        self.aflakName.setObjectName("aflakName")
        self.gridLayout.addWidget(self.aflakName, 1, 0, 1, 3)
        self.label = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)
        self.aflakAcronym = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.aflakAcronym.setFont(font)
        self.aflakAcronym.setAlignment(QtCore.Qt.AlignCenter)
        self.aflakAcronym.setObjectName("aflakAcronym")
        self.gridLayout.addWidget(self.aflakAcronym, 0, 0, 1, 3)
        self.closeButton = QtWidgets.QPushButton(AboutDialog)
        self.closeButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.closeButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 4, 0, 1, 1)
        self.versionLabel = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.versionLabel.setFont(font)
        self.versionLabel.setObjectName("versionLabel")
        self.gridLayout.addWidget(self.versionLabel, 2, 1, 1, 2)
        self.versionFixed = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.versionFixed.setFont(font)
        self.versionFixed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.versionFixed.setObjectName("versionFixed")
        self.gridLayout.addWidget(self.versionFixed, 2, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About aflak"))
        self.label_2.setText(_translate("AboutDialog", "Developed by "))
        self.aflakName.setText(_translate("AboutDialog", "Advanced Framework for Learning Astrophysical Knowledge"))
        self.label.setText(_translate("AboutDialog", "Malik Olivier Boussejra <malik@boussejra.com>"))
        self.aflakAcronym.setText(_translate("AboutDialog", "aflak"))
        self.closeButton.setText(_translate("AboutDialog", "Close"))
        self.versionLabel.setText(_translate("AboutDialog", "X.X.X"))
        self.versionFixed.setText(_translate("AboutDialog", "Version "))

