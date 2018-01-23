from astropy.io import fits


class FITS:
    def __init__(self, name, **kwargs):
        self.hdulist = fits.open(name, **kwargs)
        self.name = name
        print('Opened file: {}'.format(name))
        print(self.hdulist.info())

    def wave(self):
        return self.hdulist['WAVE'].data

    def flux(self):
        return self.hdulist['FLUX'].data

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
