import argparse

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

from fits import FITS


parser = argparse.ArgumentParser(description='Provide FITS file as input')
parser.add_argument('fits', metavar='fits-file', help='FITS file to open')

args = parser.parse_args()

fits = FITS(args.fits)

app = QtGui.QApplication([])

## Create window with ImageView widget
win = QtGui.QMainWindow()
imv = pg.ImageView()
win.setCentralWidget(imv)
win.show()
WINDOWS_TITLE = args.fits
win.setWindowTitle(WINDOWS_TITLE)

flux = fits.flux()
imv.setImage(flux)

QtGui.QApplication.instance().exec_()
