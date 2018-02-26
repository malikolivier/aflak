import threading

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
from pyqtgraph.graphicsItems.LinearRegionItem import LinearRegionItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox

from .AstroImageView_ui import Ui_Form
from .MultiROI import MultiROI, ROIType
from .WCSAxis import WCSAxes


class AstroImageView(pg.ImageView):
    """
    Extends ImageView class.
     - Replace default HistogramLUTWidget with our AstroHistogramLUTWidget.
     - Replace PlotWidget for roiPlot (defined inside UI class) by
       AstroWaveFormPlotWidget
     - Delete roiBtn
    """
    def __init__(self, parent=None, name="ImageView", view=None,
                 imageItem=None, *args):
        QtGui.QWidget.__init__(self, parent, *args)
        self.levelMax = 4096
        self.levelMin = 0
        self.name = name
        self.image = None
        self.axes = {}
        self.imageDisp = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.scene = self.ui.graphicsView.scene()

        self.ignoreTimeLine = False

        self.wcsAxes = WCSAxes()
        if view is None:
            self.view = self.wcsAxes.plotItem
        else:
            self.view = view
        self.ui.graphicsView.setCentralItem(self.view)
        self.view.setAspectLocked(True)
        self.view.invertY()

        if imageItem is None:
            self.imageItem = ImageItem()
        else:
            self.imageItem = imageItem
        self.view.addItem(self.imageItem)
        self.currentIndex = 0

        self.ui.histogram.setImageItem(self.imageItem)

        self.menu = None

        self._hideSlider()

        self.roiEnabled = False
        self.roi = MultiROI()
        self.roi.setZValue(20)
        self.view.addItem(self.roi)
        self.roi.hide()
        self.normRoi = MultiROI()
        self.normRoi.setPen('y')
        self.normRoi.setZValue(20)
        self.view.addItem(self.normRoi)
        self.normRoi.hide()
        self.roiCurve = self.ui.roiPlot.plot()
        self.timeLine = InfiniteLine(0, movable=True)
        self.timeLine.setPen((255, 255, 0, 200))
        self.timeLine.setZValue(1)
        self.ui.roiPlot.addItem(self.timeLine)
        self.ui.splitter.setSizes([self.height()-35, 35])
        self.ui.roiPlot.hideAxis('left')

        self.keysPressed = {}
        self.playTimer = QtCore.QTimer()
        self.playRate = 0
        self.lastPlayTime = 0

        self.normRgn = LinearRegionItem()
        self.normRgn.setZValue(0)
        self.ui.roiPlot.addItem(self.normRgn)
        self.normRgn.hide()

        # wrap functions from view box
        for fn in ['addItem', 'removeItem']:
            setattr(self, fn, getattr(self.view, fn))

        # wrap functions from histogram
        for fn in ['setHistogramRange', 'autoHistogramRange', 'getLookupTable',
                   'getLevels']:
            setattr(self, fn, getattr(self.ui.histogram, fn))

        self.ui.horizontalSlider.valueChanged.connect(self._sliderValueChanged)
        self.ui.sliderValueSpinBox.valueChanged.connect(self._spinBoxChanged)
        self.timeLine.sigPositionChanged.connect(self.timeLineChanged)
        self.roi.sigRegionChanged.connect(self.roiChanged)

        self.playTimer.timeout.connect(self.timeout)

        self.normProxy = pg.SignalProxy(self.normRgn.sigRegionChanged,
                                        slot=self.updateNorm)
        self.normRoi.sigRegionChangeFinished.connect(self.updateNorm)

        self.ui.roiPlot.registerPlot(self.name + '_ROI')
        self.view.register(self.name)

        self.noRepeatKeys = [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left,
                             QtCore.Qt.Key_Up, QtCore.Qt.Key_Down,
                             QtCore.Qt.Key_PageUp, QtCore.Qt.Key_PageDown]

        # initialize roi plot to correct shape / visibility
        self.setROIType(None)

    def set_fits_file(self, fitsFile):
        self.wcsAxes.setFitsFile(fitsFile)
        flux = fitsFile.flux()
        wave = fitsFile.wave()
        self.setImage(flux, xvals=wave)
        self.ui.roiPlot.setFitsFile(fitsFile)
        # TODO: Autorange the image after it is drawn.
        # This is a work around for what seems to be a bug in the
        # *pg.ArrowItem*: When arrows are shown in the canvas, the default
        # range of the axis becomes larger. Arrows are included from *WCSAxis*.
        timer = threading.Timer(0.1, lambda: self.view.vb.menu.autoRange())
        timer.start()

    def setImage(self, img, autoRange=True, autoLevels=True, levels=None,
                 axes=None, xvals=None, pos=None, scale=None, transform=None,
                 autoHistogramRange=True):
        """
        Reimplement setImage without using roiBtn
        """
        if hasattr(img, 'implements') and img.implements('MetaArray'):
            img = img.asarray()

        if not isinstance(img, np.ndarray):
            required = ['dtype', 'max', 'min', 'ndim', 'shape', 'size']
            if not all([hasattr(img, attr) for attr in required]):
                raise TypeError("Image must be NumPy array or any object "
                                "that provides compatible attributes/methods:"
                                "\n  %s" % str(required))

        self.image = img
        self.imageDisp = None

        if axes is None:
            if self.imageItem.axisOrder == 'col-major':
                x, y = (0, 1)
            else:
                x, y = (1, 0)

            if img.ndim == 2:
                self.axes = {'t': None, 'x': x, 'y': y, 'c': None}
            elif img.ndim == 3:
                # Ambiguous case; make a guess
                if img.shape[2] <= 4:
                    self.axes = {'t': None, 'x': x, 'y': y, 'c': 2}
                else:
                    self.axes = {'t': 0, 'x': x+1, 'y': y+1, 'c': None}
            elif img.ndim == 4:
                # Even more ambiguous; just assume the default
                self.axes = {'t': 0, 'x': x+1, 'y': y+1, 'c': 3}
            else:
                raise Exception("Can not interpret image with dimensions %s" %
                                str(img.shape))
        elif isinstance(axes, dict):
            self.axes = axes.copy()
        elif isinstance(axes, list) or isinstance(axes, tuple):
            self.axes = {}
            for i in range(len(axes)):
                self.axes[axes[i]] = i
        else:
            raise Exception("Can not interpret axis specification %s. "
                            "Must be like {'t': 2, 'x': 0, 'y': 1} or "
                            "('t', 'x', 'y', 'c')" % str(axes))

        for x in ['t', 'x', 'y', 'c']:
            self.axes[x] = self.axes.get(x, None)
        axes = self.axes

        if xvals is not None:
            self.tVals = xvals
        elif axes['t'] is not None:
            if hasattr(img, 'xvals'):
                try:
                    self.tVals = img.xvals(axes['t'])
                except Exception:
                    self.tVals = np.arange(img.shape[axes['t']])
            else:
                self.tVals = np.arange(img.shape[axes['t']])

        self.currentIndex = 0
        self.updateImage(autoHistogramRange=autoHistogramRange)
        if levels is None and autoLevels:
            self.autoLevels()
        # this does nothing since getProcessedImage sets these values again.
        if levels is not None:
            self.setLevels(*levels)

        if self.roiEnabled:
            self.roiChanged()

        if self.axes['t'] is not None:
            self.ui.roiPlot.setXRange(self.tVals.min(), self.tVals.max())
            self.timeLine.setValue(0)
            if len(self.tVals) > 1:
                start = self.tVals.min()
                stop = (self.tVals.max() +
                        abs(self.tVals[-1] - self.tVals[0]) * 0.02)
            elif len(self.tVals) == 1:
                start = self.tVals[0] - 0.5
                stop = self.tVals[0] + 0.5
            else:
                start = 0
                stop = 1
            for s in [self.timeLine, self.normRgn]:
                s.setBounds([start, stop])

        self.imageItem.resetTransform()
        if scale is not None:
            self.imageItem.scale(*scale)
        if pos is not None:
            self.imageItem.setPos(*pos)
        if transform is not None:
            self.imageItem.setTransform(transform)

        if autoRange:
            self.autoRange()
        self._updateRoiPlot()

    # Override normalization functions to just return the image as is
    # We do not use ImageView's normalization features (yet)
    def normalize(self, image):
        return image.view(np.ndarray).copy()

    # Override as well
    def updateNorm(self):
        pass

    def setROIType(self, roiType):
        if roiType is None:
            self.roiEnabled = False
        else:
            self.roiEnabled = True
            if roiType == ROIType.SEMIAUTOMATIC:
                self._showSlider()
            else:
                self._hideSlider()
            self.roi.setROIType(roiType)
        self._updateRoiPlot()

    def _updateRoiPlot(self):
        showRoiPlot = False
        if self.roiEnabled:
            showRoiPlot = True
            self.roi.show()
            self.ui.roiPlot.setMouseEnabled(True, True)
            self.ui.splitter.setSizes([self.height()*0.6, self.height()*0.4])
            self.roiCurve.show()
            self.roiChanged()
            self.ui.roiPlot.showAxis('left')
        else:
            self.roi.hide()
            self.ui.roiPlot.setMouseEnabled(False, False)
            self.roiCurve.hide()
            self.ui.roiPlot.hideAxis('left')

        if self.hasTimeAxis():
            showRoiPlot = True
            mn = self.tVals.min()
            mx = self.tVals.max()
            self.ui.roiPlot.setXRange(mn, mx, padding=0.01)
            self.timeLine.show()
            self.timeLine.setBounds([mn, mx])
            self.ui.roiPlot.show()
            if not self.roiEnabled:
                self.ui.splitter.setSizes([self.height()-35, 35])
        else:
            self.timeLine.hide()

        self.ui.roiPlot.setVisible(showRoiPlot)

    def _hideSlider(self):
        self.ui.horizontalSliderLabel.hide()
        self.ui.horizontalSlider.hide()
        self.ui.sliderValueSpinBox.hide()

    def _showSlider(self):
        self.ui.horizontalSliderLabel.show()
        self.ui.horizontalSlider.show()
        self.ui.sliderValueSpinBox.show()

    def _sliderValueChanged(self, value):
        spinBoxVal = value / 100.0
        self.ui.sliderValueSpinBox.setValue(spinBoxVal)
        self.roi.setSliderValue(spinBoxVal)

    def _spinBoxChanged(self, value):
        self.ui.horizontalSlider.setValue(int(value * 100))
        self.roi.setSliderValue(value)
