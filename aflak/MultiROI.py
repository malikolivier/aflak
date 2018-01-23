import enum

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from .functions import floodfill, getPath


class RectROI(pg.ROI):
    def __init__(self, size, parent=None):
        super().__init__(pos=[0, 0], size=size, parent=parent)
        self.handleSize = 15
        self.addScaleHandle([1, 1], [0, 0])
        self.addRotateHandle([0, 0], [0.5, 0.5])


class PolygonROI(pg.PolyLineROI):
    def __init__(self, positions, closed=False, pos=None, **kwargs):
        if pos is None:
            pos = [0, 0]
        self.closed = closed
        self.segments = []
        pg.ROI.__init__(self, pos, size=[1, 1], **kwargs)
        self.handleSize = 10

        self.setPoints(positions)

    def getArrayRegion(self, arr, img=None, axes=(0, 1),
                       returnMappedCoords=False, **kwds):
        """
        Fix a bug in pg.PolygonROI
        https://github.com/pyqtgraph/pyqtgraph/pull/618
        """
        if returnMappedCoords:
            sliced, mappedCoords = pg.ROI.getArrayRegion(self, arr, img, axes,
                                                         returnMappedCoords,
                                                         fromBoundingRect=True,
                                                         **kwds)
        else:
            sliced = pg.ROI.getArrayRegion(self, arr, img, axes,
                                           returnMappedCoords,
                                           fromBoundingRect=True, **kwds)

        mask = self.renderShapeMask(sliced.shape[axes[0]],
                                    sliced.shape[axes[1]])
        if img.axisOrder != 'col-major':
            mask = mask.T

        # reshape mask to ensure it is applied to the correct data axes
        shape = [1] * arr.ndim
        shape[axes[0]] = sliced.shape[axes[0]]
        shape[axes[1]] = sliced.shape[axes[1]]
        mask = mask.reshape(shape)

        if returnMappedCoords:
            return sliced * mask, mappedCoords * mask
        else:
            return sliced * mask


class EllipseROI(pg.EllipseROI):
    def __init__(self, pos, size, **kwargs):
        pg.ROI.__init__(self, pos, size, **kwargs)
        self.handleSize = 10
        self.addRotateHandle([1.0, 0.5], [0.5, 0.5])
        self.addScaleHandle([0.5*2.**-0.5 + 0.5, 0.5*2.**-0.5 + 0.5],
                            [0.5, 0.5])

    def getArrayRegion(self, arr, img=None, axes=(0, 1),
                       returnMappedCoords=False, **kwds):
        """
        Fix a bug in pg.EllipseROI
        https://github.com/pyqtgraph/pyqtgraph/pull/618
        """
        if returnMappedCoords:
            arr, mappedCoords = pg.ROI.getArrayRegion(self, arr, img, axes,
                                                      returnMappedCoords,
                                                      **kwds)
        else:
            arr = pg.ROI.getArrayRegion(self, arr, img, axes,
                                        returnMappedCoords, **kwds)
        if arr is None or arr.shape[axes[0]] == 0 or arr.shape[axes[1]] == 0:
            if returnMappedCoords:
                return arr, mappedCoords
            else:
                return arr
        w = arr.shape[axes[0]]
        h = arr.shape[axes[1]]

        # generate an ellipsoidal mask
        mask = np.fromfunction(lambda x, y: (((x+0.5)/(w/2.)-1)**2 +
                                             ((y+0.5)/(h/2.)-1)**2)**0.5 < 1,
                               (w, h))

        # reshape to match array axes
        if axes[0] > axes[1]:
            mask = mask.T
        shape = [(n if i in axes else 1) for i, n in enumerate(arr.shape)]
        mask = mask.reshape(shape)
        if returnMappedCoords:
            return arr * mask, mappedCoords * mask
        else:
            return arr * mask


class SemiAutomaticROI(pg.ROI):
    """
    Use floodfill algorithm to make the countour around a bright object.

    The whole ROI can only be moved by selecting the starting point of the
    floodfill algorithm. This starting point is a rectangular handle as defined
    in the *__init__* method.
    """
    def __init__(self, pos=(0, 0), threshold=0.9, parent=None):
        super().__init__(pos=pos, parent=parent, movable=False)
        self.handleSize = 10
        self.addHandle({'name': 'startNode', 'type': 't', 'pos': pos})
        self.threshold = threshold

    def setThreshold(self, threshold):
        self.threshold = threshold
        # Emit change in ROI and force a re-paint
        self.sigRegionChanged.emit(self)
        self.update()

    def getArrayRegion(self, arr, img, axes=(0, 1), returnMappedCoords=False):
        xStart = int(self.state['pos'][0])
        yStart = int(self.state['pos'][1])
        if (xStart < 0 or xStart > img.image.shape[0] or
                yStart < 0 or yStart > img.image.shape[1]):
            mask = np.zeros((img.image.shape[0], img.image.shape[1]),
                            dtype=bool)
        else:
            startVal = img.image[xStart, yStart]
            mask = floodfill(img.image, self.state['pos'],
                             lambda val: val >= startVal * self.threshold)
        if returnMappedCoords:
            mappedCoords = set()
            for i, line in enumerate(mask):
                for j, _ in enumerate(line):
                    mappedCoords.add((i, j))
            self.mask = mask
            return arr * mask, mappedCoords
        else:
            return arr * mask

    def boundingRect(self):
        """
        Return the bounding rectangle of the ROI. The bounding rectangle of the
        ROI is set as the full image (the biggest size the ROI can be) to work
        around what seems to be PyQt painting bug.
        It seems that objects painted outside the bounding rectangle are not
        correctly deleted during a re-paint.

        The bounding rectangle is returned via the mask of the ROI, which is
        only computed after *getArrayRegion* with *returnMappedCoords=True* in
        run.
        """
        if not hasattr(self, 'mask'):
            return QtCore.QRectF()
        else:
            rect = QtCore.QRectF(0, 0, self.mask.shape[0], self.mask.shape[1])
            rect.translate(-self.state['pos'][0], -self.state['pos'][1])
            return rect

    def paint(self, p, opt, widget):
        """
        Paint the path of the ROI using *self.mask*. *self.mask* is only
        computed after *getArrayRegion* with *returnMappedCoords=True* in run.
        """
        if not hasattr(self, 'mask'):
            return
        p.translate(-self.state['pos'][0], -self.state['pos'][1])
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setPen(self.currentPen)

        p.drawPath(getPath(self.mask))


class ROIType(enum.Enum):
    ELLIPSE = EllipseROI
    POLYGON = PolygonROI
    RECTANGLE = RectROI
    SEMIAUTOMATIC = SemiAutomaticROI


class MultiROI(QtGui.QGraphicsObject):
    """
    Container for several type of ROIs.
    This class in itself is only defining the interface between the currently
    selected ROI type and the outside world.

    A few abstract methods from QGraphicsObject must be overridden
    (*boundingRect* and *paint*) for integration with Qt.
    """
    sigRegionChangeFinished = QtCore.Signal(object)
    sigRegionChangeStarted = QtCore.Signal(object)
    sigRegionChanged = QtCore.Signal(object)

    def __init__(self):
        super().__init__()
        self.currentRoi = None
        self.cachedRois = {}
        self.setROIType(ROIType.RECTANGLE)

        # Wrap methods from *currentRoi*
        for fnName in ['setZValue', 'zValue', 'scene', 'setPen',
                       'getArrayRegion']:
            def _create_method(name):
                def method(*args, **kwargs):
                    fn = getattr(self.currentRoi, name)
                    return fn(*args, **kwargs)
                method.__name__ = name
                return method
            setattr(self, fnName, _create_method(fnName))
        del _create_method

    def boundingRect(self):
        return QtCore.QRectF()

    def paint(self, *args):
        pass

    def setROIType(self, roiType):
        self._disconnectAll()

        if roiType in self.cachedRois:
            self.currentRoi = self.cachedRois[roiType]
        else:
            if roiType == ROIType.ELLIPSE:
                self.currentRoi = EllipseROI([10, 10], [10, 10], parent=self)
            elif roiType == ROIType.POLYGON:
                self.currentRoi = PolygonROI([[0, 0], [5, 0],
                                              [6, 6], [0, 5]],
                                             closed=True, parent=self)
            elif roiType == ROIType.RECTANGLE:
                self.currentRoi = RectROI(10, parent=self)
            elif roiType == ROIType.SEMIAUTOMATIC:
                self.currentRoi = SemiAutomaticROI(parent=self)
            else:
                raise NotImplemented('Unhandled ROIType: %s' % repr(roiType))
            self.cachedRois[roiType] = self.currentRoi

        # Hide all ROIs expect the selected type
        for cachedRoiType, cachedRoi in self.cachedRois.items():
            if cachedRoiType == roiType:
                cachedRoi.show()
            else:
                cachedRoi.hide()

        self._connectAll()
        self.sigRegionChanged.emit(self)

    def _disconnectAll(self):
        if self.currentRoi is not None:
            self.currentRoi.sigRegionChanged.disconnect(self.roiChangedEvent)
            self.currentRoi.sigRegionChangeStarted.disconnect(
                self.roiChangeStartedEvent)
            self.currentRoi.sigRegionChangeFinished.disconnect(
                self.roiChangeFinishedEvent)

    def _connectAll(self):
        self.currentRoi.sigRegionChanged.connect(self.roiChangedEvent)
        self.currentRoi.sigRegionChangeStarted.connect(
            self.roiChangeStartedEvent)
        self.currentRoi.sigRegionChangeFinished.connect(
            self.roiChangeFinishedEvent)

    def setSliderValue(self, value):
        if isinstance(self.currentRoi, ROIType.SEMIAUTOMATIC.value):
            self.currentRoi.setThreshold(value)

    def roiChangedEvent(self):
        self.sigRegionChanged.emit(self)

    def roiChangeStartedEvent(self):
        self.sigRegionChangeStarted.emit(self)

    def roiChangeFinishedEvent(self):
        self.sigRegionChangeFinished.emit(self)
