from pyqtgraph.Qt import QtGui

from aflak.mainwindow import MainWindow


def test_set_fits_file():
    app = QtGui.QApplication([])
    main = MainWindow()
    main.set_fits_file("data/manga-7443-12703-LINCUBE.fits")
