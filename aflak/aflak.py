import argparse

from pyqtgraph.Qt import QtGui

import aflak.mainwindow


def main():
    parser = argparse.ArgumentParser(description='Provide FITS file as input')
    parser.add_argument('fits', metavar='fits-file', nargs='?',
                        help='FITS file to open')

    args = parser.parse_args()

    app = QtGui.QApplication([])
    main = aflak.mainwindow.MainWindow()
    if args.fits is not None:
        main.set_fits_file(args.fits)

    return QtGui.QApplication.instance().exec_()
