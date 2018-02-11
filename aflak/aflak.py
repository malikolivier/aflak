import argparse

from pyqtgraph.Qt import QtGui

from aflak.__init__ import __version__
import aflak.mainwindow


def main():
    parser = argparse.ArgumentParser(description='Provide FITS file as input')
    parser.add_argument('fits', metavar='fits-file', nargs='?',
                        help='FITS file to open')
    parser.add_argument('-v', '--version', action='version',
                        version='aflak {}'.format(__version__))

    args = parser.parse_args()

    app = QtGui.QApplication([])
    main = aflak.mainwindow.MainWindow()
    if args.fits is not None:
        main.set_fits_file(args.fits)

    main.show()
    return QtGui.QApplication.instance().exec_()
