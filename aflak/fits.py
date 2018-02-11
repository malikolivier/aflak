import enum

from astropy import wcs
from astropy.io import fits
import numpy as np


class FITSUnit(enum.Enum):
    DEGREE = 1


class FITS:
    def __init__(self, name, **kwargs):
        self.hdulist = fits.open(name, **kwargs)
        self.name = name
        self.wcs = wcs.WCS(self.hdulist['FLUX'].header)
        print('Opened file: {}'.format(name))
        print(self.hdulist.info())

    def wave(self):
        return self.hdulist['WAVE'].data

    def flux(self):
        """
        Get flux data with an alignment such as the north direction is pointing
        up.
        """
        # Swap x/wave axes, rotate and then swap axes back
        swapped = self.hdulist['FLUX'].data.swapaxes(0, 2)
        return np.rot90(swapped).swapaxes(0, 2)

    def wave_unit(self):
        """
        Return the unit of the waveform in a suitable format to be displayed on
        a plot, if possible.
        """
        if 'CUNIT3' in self.hdulist['FLUX'].header:
            raw_unit = self.hdulist['FLUX'].header['CUNIT3']
            if raw_unit == 'Angstrom':
                return 'Å'
            else:
                return raw_unit

    def flux_unit(self):
        if 'BUNIT' in self.hdulist['FLUX'].header:
            return self.hdulist['FLUX'].header['BUNIT']

    def summed_flux_unit(self):
        flux_unit = self.flux_unit()
        if flux_unit is not None:
            return flux_unit.replace("/Ang", "")

    def reference_pixel(self, axis: int) -> float:
        key = 'CRPIX{}'.format(axis)
        if key in self.hdulist['FLUX'].header:
            # In FITS files, indexing start from 1 (like FORTRAN)
            return float(self.hdulist['FLUX'].header[key]) - 1
        else:
            raise KeyError('Unknown axis "{}". '
                           'Key not found: "{}"'.format(axis, key))

    def pixel_count(self, axis: int) -> float:
        key = 'NAXIS{}'.format(axis)
        if key in self.hdulist['FLUX'].header:
            return float(self.hdulist['FLUX'].header[key])
        else:
            raise KeyError('Unknown axis "{}". '
                           'Key not found: "{}"'.format(axis, key))

    def convert_to_wcs(self, pixel: (float, float)) -> [float, float]:
        x = pixel[0]
        y_axis_len = self.hdulist['FLUX'].data.shape[2]
        y = y_axis_len - pixel[1]
        return self.wcs.all_pix2world([[x, y, 1]], 1)[0, 0:2]

    def unit(self, axis: int) -> FITSUnit or str:
        key = 'CUNIT{}'.format(axis)
        if key in self.hdulist['FLUX'].header:
            unit = self.hdulist['FLUX'].header[key]
            if unit == 'deg':
                return FITSUnit.DEGREE
            else:
                return unit
        else:
            raise KeyError('Unknown axis "{}". '
                           'Key not found: "{}"'.format(axis, key))

    def get_north_angle(self) -> float:
        ref1 = self.reference_pixel(1)
        ref2 = self.reference_pixel(2)
        ref_wcoords = self.wcs.all_pix2world([[ref1, ref2, 1]], 1)[0]
        northern_point = self.wcs.all_world2pix([[ref_wcoords[0],
                                                  ref_wcoords[1] + 1,
                                                  ref_wcoords[2]]], 1)[0, 0:2]
        northern_vector = northern_point - np.array([ref1, ref2])
        return np.arctan2(northern_point[1], northern_point[0])

    def get_east_angle(self) -> float:
        ref1 = self.reference_pixel(1)
        ref2 = self.reference_pixel(2)
        ref_wcoords = self.wcs.all_pix2world([[ref1, ref2, 1]], 1)[0]
        eastern_point = self.wcs.all_world2pix([[ref_wcoords[0] - 1,
                                                 ref_wcoords[1],
                                                 ref_wcoords[2]]], 1)[0, 0:2]
        eastern_vector = eastern_point - np.array([ref1, ref2])
        return np.arctan2(eastern_vector[1], eastern_vector[0])
