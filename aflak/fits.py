import enum

from astropy import wcs
from astropy.io import fits
import numpy as np


class FITSUnit(enum.Enum):
    DEGREE = 1


STR_UNITS_TO_FITSUNITS = {
    'deg': FITSUnit.DEGREE
}

UNITS_ON_PLOT = {
    'Angstrom': 'Å'
}


def generate_fits_props(hdulist):
    """
    1. Find FLUX/WAVE hdu if they exist. Then get relevant data for each HDU.
    2. Fallback: If they do not exist, try to get relevant data from primary
       HDU.

       props = {
           'flux_data': None,
           'wave_data': None,
           'flux_unit': None,
           'wave_unit': None,
           'reference_pixels': {
               0: None, # CRPIX_:
           },
           'pixel_count': {
               0: None, # NAXIS_:
           }
           'units': {
               0: None, # CUNIT_:
           },
           'wcs': None,
       }
    """
    props = {}
    if 'FLUX' in hdulist and 'WAVE' in hdulist:
        flux_hdu = hdulist['FLUX']
        wave_hdu = hdulist['WAVE']
        # Set 'flux_data'
        # Get flux data with an alignment such as the north direction is
        # pointing up.
        # Swap x/wave axes, rotate and then swap axes back
        swapped = flux_hdu.data.swapaxes(0, 2)
        props['flux_data'] = np.rot90(swapped).swapaxes(0, 2)
        # Set 'wave_data'
        props['wave_data'] = wave_hdu.data
        # Set 'flux_unit'
        if 'BUNIT' in flux_hdu.header:
            props['flux_unit'] = flux_hdu.header['BUNIT']
        else:
            props['flux_unit'] = None
        # Set 'wave_unit'
        # Return the unit of the waveform in a suitable format to be displayed
        # on a plot, if possible.
        if 'CUNIT3' in flux_hdu.header:
            raw_unit = flux_hdu.header['CUNIT3']
            if raw_unit in UNITS_ON_PLOT:
                props['wave_unit'] = UNITS_ON_PLOT[raw_unit]
            else:
                props['wave_unit'] = raw_unit
        # Set 'reference_pixels'
        pixels = {}
        for axis in range(1, flux_hdu.header['NAXIS'] + 1):
            key = 'CRPIX{}'.format(axis)
            # In FITS files, indexing start from 1 (like FORTRAN)
            pixels[axis] = float(flux_hdu.header[key]) - 1
        props['reference_pixels'] = pixels
        # Set 'pixel_count'
        pixel_count = {}
        for axis in range(1, flux_hdu.header['NAXIS'] + 1):
            key = 'NAXIS{}'.format(axis)
            pixel_count[axis] = float(flux_hdu.header[key])
        props['pixel_count'] = pixel_count
        # Set 'units'
        units = {}
        for axis in range(1, flux_hdu.header['NAXIS'] + 1):
            key = 'CUNIT{}'.format(axis)
            raw_unit = flux_hdu.header[key]
            if raw_unit in STR_UNITS_TO_FITSUNITS:
                units[axis] = STR_UNITS_TO_FITSUNITS[raw_unit]
            else:
                units[axis] = raw_unit
        props['units'] = units
        # Set 'wcs'
        props['wcs'] = wcs.WCS(flux_hdu.header)
    else:
        primary_hdu = hdulist[0]
        props['flux_data'] = primary_hdu.data
        props['wave_data'] = np.array(range(primary_hdu.data.shape[2]))
        # TODO
        props['flux_unit'] = ""
        props['wave_unit'] = ""
        props['reference_pixels'] = { 1: 0, 2: 0, 3: 0}
        props['pixel_count'] = { 1: 2071, 2: 303, 3: 709}
        props['units'] = { 1: "", 2: "", 3: ""}
        props['wcs'] = wcs.WCS(primary_hdu.header)
    return props


class FITS:
    @property
    def wcs(self):
        return self._props['wcs']

    def __init__(self, name, **kwargs):
        self.hdulist = fits.open(name, **kwargs)
        self.name = name
        self._props = generate_fits_props(self.hdulist)
        print('Opened file: {}'.format(name))
        print(self.hdulist.info())

    def wave(self):
        return self._props['wave_data']

    def flux(self):
        return self._props['flux_data']

    def wave_unit(self):
        return self._props['wave_unit']

    def flux_unit(self):
        return self._props['flux_unit']

    def summed_flux_unit(self):
        flux_unit = self.flux_unit()
        if flux_unit is not None:
            return flux_unit.replace("/Ang", "")

    def reference_pixel(self, axis: int) -> float:
        return self._props['reference_pixels'][axis]

    def pixel_count(self, axis: int) -> float:
        return self._props['pixel_count'][axis]

    def convert_to_wcs(self, pixel: (float, float)) -> [float, float]:
        x = pixel[0]
        y_axis_len = self._props['flux_data'].shape[2]
        y = y_axis_len - pixel[1]
        return self.wcs.all_pix2world([[x, y, 1]], 1)[0, 0:2]

    def unit(self, axis: int) -> FITSUnit or str:
        return self._props['units'][axis]

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
