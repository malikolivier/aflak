import sys

import numpy as np
import pyqtgraph as pg

from .fits import FITSUnit


class WCSAxes:
    def __init__(self):
        self.bottom = WCSAxis(orientation='bottom')

    def setFitsFile(self, fitsFile):
        self.bottom.setFitsFile(fitsFile)


class WCSAxis(pg.AxisItem):
    def __init__(self, orientation, fitsFile=None, **kwargs):
        super().__init__(orientation, **kwargs)
        self.fitsFile = fitsFile

    def setFitsFile(self, fitsFile):
        self.fitsFile = fitsFile

    def tickSpacing(self, minVal, maxVal, size):
        original = super().tickSpacing(minVal, maxVal, size)
        ref = self.fitsFile.reference_pixel(1)
        return [(spacing, offset + ref) for spacing, offset in original]

    def tickStrings(self, values, scale, spacing):
        ref = self.fitsFile.reference_pixel(1)
        unit = self.fitsFile.unit(1)
        ref_wcs = self.fitsFile.convert_to_wcs((ref, 0))[0]
        strings = []
        for v in values:
            coords = self.fitsFile.convert_to_wcs((v, 0))
            if unit == FITSUnit.DEGREE:
                abs_coords = '%.4f°' % coords[0]
                rel_arcsec = (coords[0] - ref_wcs) * 3600
                if rel_arcsec == 0:
                    rel_arcsec = ''
                else:
                    rel_arcsec = "%.2e''" % rel_arcsec
            else:
                abs_coord = '%.4f %s' % (coords[0], unit)
                # Cannot convert to arc second, as unit is unknown!
                rel_arcsec = '%.2e %s' % ((coords[0] - ref_wcs) * 3600, unit)
            string = "\n%d\n%s\n%s\n" % (v - ref, abs_coords, rel_arcsec)
            strings.append(string)
        return strings
