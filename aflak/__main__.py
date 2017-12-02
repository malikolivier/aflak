import argparse

from pyqtgraph.Qt import QtGui

import aflak.window


parser = argparse.ArgumentParser(description='Provide FITS file as input')
parser.add_argument('fits', metavar='fits-file', nargs='?',
                    help='FITS file to open')

args = parser.parse_args()

app = QtGui.QApplication([])
aflak = aflak.window.MainWindow()
if args.fits is not None:
    aflak.set_fits_file(args.fits)

QtGui.QApplication.instance().exec_()


# An entry point is merely added so that setuptools finds it and
# launches this script
def _main():
    pass
