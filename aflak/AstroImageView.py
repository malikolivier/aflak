import pyqtgraph as pg

import aflak.fits


class AstroImageView(pg.ImageView):
    def __init__(self, *args, **kwargs):
        pg.ImageView.__init__(self, *args, **kwargs)

    def set_fits_file(self, file_path):
        my_fits = aflak.fits.FITS(file_path)
        flux = my_fits.flux()
        wave = my_fits.wave()
        self.setImage(flux, xvals=wave)
