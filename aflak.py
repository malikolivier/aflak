import argparse

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtWidgets

from fits import FITS


parser = argparse.ArgumentParser(description='Provide FITS file as input')
parser.add_argument('fits', metavar='fits-file', help='FITS file to open')

args = parser.parse_args()

fits = FITS(args.fits)

app = QtGui.QApplication([])

# Create window with ImageView widget
win = QtGui.QMainWindow()

# Add menu bar to window
exitAction = QtGui.QAction('&Exit', win)
exitAction.setShortcut('Ctrl+Q')
exitAction.triggered.connect(QtWidgets.qApp.quit)

menubar = win.menuBar()
fileMenu = menubar.addMenu('&File')
fileMenu.addAction(exitAction)


imv = pg.ImageView()
win.setCentralWidget(imv)
win.show()
WINDOWS_TITLE = args.fits
win.setWindowTitle(WINDOWS_TITLE)

flux = fits.flux()
wave = fits.wave()
imv.setImage(flux, xvals=wave)

QtGui.QApplication.instance().exec_()
