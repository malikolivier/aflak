from astropy.io import fits


class FITS:
    def __init__(self, name, **kwargs):
        self.hdulist = fits.open(name, **kwargs)
        print('Opened file: {}'.format(name))
        print(self.hdulist.info())

    def wave(self):
        return self.hdulist['WAVE'].data

    def flux(self):
        return self.hdulist['FLUX'].data
