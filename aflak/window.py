from pyqtgraph.Qt import QtGui, QtWidgets

import viewer


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

        self.viewer = viewer.AstroImageViewer()
        self.win.setCentralWidget(self.viewer.imv)
        self.win.show()

    def set_fits_file(self, file_path):
        self.win.setWindowTitle(file_path)
        self.viewer.set_fits_file(file_path)
