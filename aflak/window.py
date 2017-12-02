import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtWidgets

import fits


class MainWindow:
    def __init__(self):
        # Create self.window with ImageView widget
        self.win = QtGui.QMainWindow()
        # Add menu bar to self.window
        exitAction = QtGui.QAction('&Exit', self.win)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        menubar = self.win.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self._imv = pg.ImageView()
        self.win.setCentralWidget(self._imv)
        self.win.show()

    def set_fits_file(self, file_path):
        self.win.setWindowTitle(file_path)
        my_fits = fits.FITS(file_path)
        flux = my_fits.flux()
        wave = my_fits.wave()
        self._imv.setImage(flux, xvals=wave)
