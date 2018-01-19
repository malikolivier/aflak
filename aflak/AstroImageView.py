import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.graphicsItems.ImageItem import ImageItem
from pyqtgraph.graphicsItems.InfiniteLine import InfiniteLine
from pyqtgraph.graphicsItems.LinearRegionItem import LinearRegionItem
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from pyqtgraph.imageview.ImageView import PlotROI

from .AstroImageView_ui import Ui_Form


class AstroImageView(pg.ImageView):
    """
    Extends ImageView class.
     - Replace default HistogramLUTWidget with our AstroHistogramLUTWidget.
     - Replace PlotWidget for roiPlot (defined inside UI class) by
       AstroWaveFormPlotWidget
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

        if view is None:
            self.view = ViewBox()
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

        self.ui.normGroup.hide()

        self.roi = PlotROI(10)
        self.roi.setZValue(20)
        self.view.addItem(self.roi)
        self.roi.hide()
        self.normRoi = PlotROI(10)
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

        self.timeLine.sigPositionChanged.connect(self.timeLineChanged)
        self.ui.roiBtn.clicked.connect(self.roiClicked)
        self.roi.sigRegionChanged.connect(self.roiChanged)

        self.ui.menuBtn.clicked.connect(self.menuClicked)
        self.ui.normDivideRadio.clicked.connect(self.normRadioChanged)
        self.ui.normSubtractRadio.clicked.connect(self.normRadioChanged)
        self.ui.normOffRadio.clicked.connect(self.normRadioChanged)
        self.ui.normROICheck.clicked.connect(self.updateNorm)
        self.ui.normFrameCheck.clicked.connect(self.updateNorm)
        self.ui.normTimeRangeCheck.clicked.connect(self.updateNorm)
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
        self.roiClicked()

    def set_fits_file(self, fitsFile):
        flux = fitsFile.flux()
        wave = fitsFile.wave()
        self.setImage(flux, xvals=wave)
        self.ui.roiPlot.setFitsFile(fitsFile)

    def roiClicked(self):
        super().roiClicked()
        self.ui.roiPlot.updateAstroDisplay(show=self.ui.roiBtn.isChecked())
