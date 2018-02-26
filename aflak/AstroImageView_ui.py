# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aflak/AstroImageViewTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(837, 588)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = GraphicsView(self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 2, 0, 2, 1)
        self.sliderHorizontalLayout = QtWidgets.QHBoxLayout()
        self.sliderHorizontalLayout.setObjectName("sliderHorizontalLayout")
        self.horizontalSliderLabel = QtWidgets.QLabel(self.layoutWidget)
        self.horizontalSliderLabel.setObjectName("horizontalSliderLabel")
        self.sliderHorizontalLayout.addWidget(self.horizontalSliderLabel)
        self.horizontalSlider = QtWidgets.QSlider(self.layoutWidget)
        self.horizontalSlider.setEnabled(True)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(0)
        self.horizontalSlider.setProperty("value", 90)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.sliderHorizontalLayout.addWidget(self.horizontalSlider)
        self.gridLayout.addLayout(self.sliderHorizontalLayout, 0, 0, 1, 1)
        self.sliderValueSpinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.sliderValueSpinBox.setMaximum(1.0)
        self.sliderValueSpinBox.setSingleStep(0.1)
        self.sliderValueSpinBox.setProperty("value", 0.9)
        self.sliderValueSpinBox.setObjectName("sliderValueSpinBox")
        self.gridLayout.addWidget(self.sliderValueSpinBox, 0, 2, 1, 1)
        self.histogram = AstroHistogramLUTWidget(self.layoutWidget)
        self.histogram.setObjectName("histogram")
        self.gridLayout.addWidget(self.histogram, 2, 2, 1, 1)
        self.roiPlot = AstroWaveFormPlotWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.roiPlot.sizePolicy().hasHeightForWidth())
        self.roiPlot.setSizePolicy(sizePolicy)
        self.roiPlot.setMinimumSize(QtCore.QSize(0, 40))
        self.roiPlot.setObjectName("roiPlot")
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.horizontalSliderLabel.setText(_translate("Form", " ROI Threshold "))

from .AstroHistogramLUTWidget import AstroHistogramLUTWidget
from .AstroWaveFormPlotWidget import AstroWaveFormPlotWidget
from pyqtgraph.widgets.GraphicsView import GraphicsView
