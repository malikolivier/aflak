# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aflak/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.astroImageView = AstroImageView(MainWindow)
        self.astroImageView.setObjectName("astroImageView")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFITS = QtWidgets.QMenu(self.menubar)
        self.menuFITS.setEnabled(False)
        self.menuFITS.setObjectName("menuFITS")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAnalyze = QtWidgets.QMenu(self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSee_FITS_header = QtWidgets.QAction(MainWindow)
        self.actionSee_FITS_header.setObjectName("actionSee_FITS_header")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRectangular_ROI = QtWidgets.QAction(MainWindow)
        self.actionRectangular_ROI.setCheckable(True)
        self.actionRectangular_ROI.setObjectName("actionRectangular_ROI")
        self.actionElliptic_ROI = QtWidgets.QAction(MainWindow)
        self.actionElliptic_ROI.setCheckable(True)
        self.actionElliptic_ROI.setObjectName("actionElliptic_ROI")
        self.actionPolygonal_ROI = QtWidgets.QAction(MainWindow)
        self.actionPolygonal_ROI.setCheckable(True)
        self.actionPolygonal_ROI.setObjectName("actionPolygonal_ROI")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuFITS.addAction(self.actionSee_FITS_header)
        self.menuHelp.addAction(self.actionAbout)
        self.menuAnalyze.addSeparator().setText("ROI")
        self.menuAnalyze.addAction(self.actionElliptic_ROI)
        self.menuAnalyze.addAction(self.actionPolygonal_ROI)
        self.menuAnalyze.addAction(self.actionRectangular_ROI)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFITS.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aflak"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFITS.setTitle(_translate("MainWindow", "FITS"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAnalyze.setTitle(_translate("MainWindow", "Analyze"))
        self.actionOpen.setText(_translate("MainWindow", "Open FITS"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSee_FITS_header.setText(_translate("MainWindow", "See FITS header"))
        self.actionSee_FITS_header.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionRectangular_ROI.setText(_translate("MainWindow", "Rectangular ROI"))
        self.actionElliptic_ROI.setText(_translate("MainWindow", "Elliptic ROI"))
        self.actionPolygonal_ROI.setText(_translate("MainWindow", "Polygonal ROI"))

from .AstroImageView import AstroImageView
