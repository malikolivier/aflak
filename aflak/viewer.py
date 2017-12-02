import pyqtgraph as pg

import aflak.fits


class AstroImageViewer:
    def __init__(self):
        self.imv = pg.ImageView()

    def set_fits_file(self, file_path):
        my_fits = aflak.fits.FITS(file_path)
        flux = my_fits.flux()
        wave = my_fits.wave()
        self.imv.setImage(flux, xvals=wave)
