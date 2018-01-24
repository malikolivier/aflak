import sys

import numpy as np
import pyqtgraph as pg

from .fits import FITSUnit


class WCSAxes:
    def __init__(self):
        self.bottom = WCSAxis(orientation='bottom')
        self.top = WCSAxis(orientation='top')
        self.left = WCSAxis(orientation='left')
        self.right = WCSAxis(orientation='right')

    def setFitsFile(self, fitsFile):
        self.bottom.setFitsFile(fitsFile)
        self.top.setFitsFile(fitsFile)
        self.left.setFitsFile(fitsFile)
        self.right.setFitsFile(fitsFile)


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
        ref = self.fitsFile.reference_pixel(self.getAxisNumber())
        return [(spacing, offset + ref) for spacing, offset in original]

    def tickStrings(self, values, scale, spacing):
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
            string = "\n%d\n%s\n%s\n" % (v - ref, abs_coords, rel_arcsec)
            strings.append(string)
        return strings
