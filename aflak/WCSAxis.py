import sys

import numpy as np
import pyqtgraph as pg
import pyqtgraph.functions as fn

from .fits import FITSUnit
from .functions import makeArrowPath


class From0ArrowItem(pg.ArrowItem):
    """
    Extends *pg.ArrowItem* so that the arrow's origin is not on the tip, but on
    the tail. This is necessary to make a good-looking compass.
    """
    def setStyle(self, **opts):
        self.opts.update(opts)

        opt = dict([(k, self.opts[k]) for k in ['headLen', 'tipAngle',
                                                'baseAngle', 'tailLen',
                                                'tailWidth']])
        self.path = makeArrowPath(opt['headLen'], opt['tipAngle'],
                                  opt['tailLen'], opt['tailWidth'])
        self.setPath(self.path)

        self.setPen(fn.mkPen(self.opts['pen']))
        self.setBrush(fn.mkBrush(self.opts['brush']))

        if self.opts['pxMode']:
            self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        else:
            self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)


class Compass:
    def __init__(self, plotItem):
        self.northArrow = From0ArrowItem(angle=90, tipAngle=30, baseAngle=10,
                                         headLen=20, tailLen=20, tailWidth=4,
                                         brush='r')
        self.northArrow.setPos(10, 10)
        self.northArrow.setZValue(1)
        self.eastArrow = From0ArrowItem(angle=0, tipAngle=30, baseAngle=10,
                                        headLen=20, tailLen=20, tailWidth=4,
                                        brush='b')
        self.eastArrow.setPos(10, 10)
        self.eastArrow.setZValue(1)
        self.hide()
        plotItem.addItem(self.northArrow)
        plotItem.addItem(self.eastArrow)

    def setFromFitsFile(self, fitsFile):
        self.northArrow.setStyle(angle=fitsFile.get_north_angle())
        self.northArrow.show()
        self.eastArrow.setStyle(angle=fitsFile.get_east_angle())
        self.eastArrow.show()

    def hide(self):
        self.northArrow.hide()
        self.eastArrow.hide()


class WCSAxes:
    def __init__(self):
        self.bottom = WCSAxis(orientation='bottom')
        self.top = WCSAxis(orientation='top')
        self.left = WCSAxis(orientation='left')
        self.right = WCSAxis(orientation='right')
        self.plotItem = pg.PlotItem(axisItems={
            'top': self.top,
            'bottom': self.bottom,
            'left': self.left,
            'right': self.right
        })
        # By default, top and right axes are not shown
        self.plotItem.showAxis('top', True)
        self.plotItem.showAxis('right', True)
        self.plotItem.showGrid(True, True)
        self.compass = Compass(self.plotItem)

    def setFitsFile(self, fitsFile):
        self.bottom.setFitsFile(fitsFile)
        self.top.setFitsFile(fitsFile)
        self.left.setFitsFile(fitsFile)
        self.right.setFitsFile(fitsFile)
        self.compass.setFromFitsFile(fitsFile)


class WCSAxis(pg.AxisItem):
    def __init__(self, orientation, fitsFile=None, **kwargs):
        super().__init__(orientation, **kwargs)
        self.fitsFile = fitsFile

    def setFitsFile(self, fitsFile):
        self.fitsFile = fitsFile

    def getAxisNumber(self):
        if self.orientation == 'bottom' or self.orientation == 'top':
            return 1
        else:
            return 2

    def toWcs(self, x: float) -> float:
        if self.orientation == 'bottom':
            return self.fitsFile.convert_to_wcs((x, 0))[0]
        elif self.orientation == 'top':
            N = self.fitsFile.pixel_count(self.getAxisNumber())
            return self.fitsFile.convert_to_wcs((x, N))[0]
        elif self.orientation == 'left':
            return self.fitsFile.convert_to_wcs((0, x))[1]
        elif self.orientation == 'right':
            N = self.fitsFile.pixel_count(self.getAxisNumber())
            return self.fitsFile.convert_to_wcs((N, x))[1]
        else:
            raise NotImplementedError('Unexpected orientation: '
                                      '%s' % self.orientation)

    def tickSpacing(self, minVal, maxVal, size):
        original = super().tickSpacing(minVal, maxVal, size)
        if self.fitsFile is None:
            return original
        ref = self.fitsFile.reference_pixel(self.getAxisNumber())
        return [(spacing, offset + ref) for spacing, offset in original]

    def tickStrings(self, values, scale, spacing):
        if self.fitsFile is None:
            return super().tickStrings(values, scale, spacing)
        ref = self.fitsFile.reference_pixel(self.getAxisNumber())
        unit = self.fitsFile.unit(self.getAxisNumber())
        ref_wcs = self.toWcs(ref)
        strings = []
        for v in values:
            coords = self.toWcs(v)
            if unit == FITSUnit.DEGREE:
                abs_coords = '%.4f°' % coords
                rel_arcsec = (coords - ref_wcs) * 3600
                if rel_arcsec == 0:
                    rel_arcsec = ''
                else:
                    rel_arcsec = "%.2e''" % rel_arcsec
            else:
                abs_coord = '%.4f %s' % (coords, unit)
                # Cannot convert to arc second, as unit is unknown!
                rel_arcsec = '%.2e %s' % ((coords - ref_wcs) * 3600, unit)
            # For top and right axis, only show the relative value in arcsec
            if self.orientation == 'top':
                string = '\n%s' % ('0' if rel_arcsec == '' else rel_arcsec)
            elif self.orientation == 'right':
                string = '0' if rel_arcsec == '' else rel_arcsec
            else:
                string = "%d\n%s\n%s" % (v - ref, abs_coords, rel_arcsec)
            if self.orientation == 'bottom':
                # Add space above to avoid overlapping of axis and labels
                string = '\n%s\n' % string
            strings.append(string)
        return strings
