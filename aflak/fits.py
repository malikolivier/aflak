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


def get_wave_unit(hdu):
    for key in ['CUNIT3', 'CTYPE3']:
        if key in hdu.header:
            raw_unit = hdu.header[key]
            return UNITS_ON_PLOT.get(raw_unit, raw_unit)


def get_reference_pixels(hdu):
    pixels = {}
    for axis in range(1, hdu.header['NAXIS'] + 1):
        key = 'CRPIX{}'.format(axis)
        # In FITS files, indexing start from 1 (like FORTRAN)
        pixels[axis] = float(hdu.header[key]) - 1
    return pixels


def get_pixel_count(hdu):
    pixel_count = {}
    for axis in range(1, hdu.header['NAXIS'] + 1):
        key = 'NAXIS{}'.format(axis)
        pixel_count[axis] = float(hdu.header[key])
    return pixel_count


def get_units(hdu):
    units = {}
    for axis in range(1, hdu.header['NAXIS'] + 1):
        key = 'CUNIT{}'.format(axis)
        for key in ['CUNIT{}'.format(axis), 'CTYPE{}'.format(axis)]:
            if key in hdu.header:
                raw_unit = hdu.header[key]
                units[axis] = STR_UNITS_TO_FITSUNITS.get(raw_unit, raw_unit)
                break
    return units


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
        props['flux_unit'] = flux_hdu.header.get('BUNIT')
        # Set 'wave_unit'
        # Return the unit of the waveform in a suitable format to be displayed
        # on a plot, if possible.
        props['wave_unit'] = get_wave_unit(flux_hdu)
        # Set 'reference_pixels'
        props['reference_pixels'] = get_reference_pixels(flux_hdu)
        # Set 'pixel_count'
        props['pixel_count'] = get_pixel_count(flux_hdu)
        # Set 'units'
        props['units'] = get_units(flux_hdu)
        # Set 'wcs'
        props['wcs'] = wcs.WCS(flux_hdu.header)
    else:
        primary_hdu = hdulist[0]
        w = wcs.WCS(primary_hdu.header)
        swapped = primary_hdu.data.swapaxes(0, 2)
        flux = np.rot90(swapped).swapaxes(0, 2)
        # flux may contain a lot of negative garbage data. Remove them all
        flux[flux <= -100] = np.nan
        props['flux_data'] = flux
        # Set 'wave_data'
        pix_coords = np.array(
            [[0, 0, i] for i in range(primary_hdu.data.shape[0])],
            np.float
        )
        props['wave_data'] = w.all_pix2world(pix_coords, 0)[:, 2]
        props['flux_unit'] = primary_hdu.header.get('BUNIT')
        props['wave_unit'] = get_wave_unit(primary_hdu)
        props['reference_pixels'] = get_reference_pixels(primary_hdu)
        props['pixel_count'] = get_pixel_count(primary_hdu)
        props['units'] = get_units(primary_hdu)
        props['wcs'] = w
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
