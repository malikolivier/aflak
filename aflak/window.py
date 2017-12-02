from pyqtgraph.Qt import QtGui, QtWidgets

import aflak.viewer


class MainWindow:
    def __init__(self):
        # Create self.window with ImageView widget
        self.win = QtGui.QMainWindow()
        # Add menu bar to self.window
        exitAction = QtGui.QAction('&Exit', self.win)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        openAction = QtGui.QAction('&Open', self.win)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self._open_file)

        menubar = self.win.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        self.viewer = aflak.viewer.AstroImageViewer()
        self.win.setCentralWidget(self.viewer.imv)
        self.win.show()

    def set_fits_file(self, file_path):
        self.win.setWindowTitle(file_path)
        self.viewer.set_fits_file(file_path)

    def _open_file(self):
        name, _file_type = QtGui.QFileDialog.getOpenFileName(self.win,
                                                             'Open File')
        # `name' is an empty string if the user pressed `Cancel' in the
        # open-file dialog
        if name != '':
            self.set_fits_file(name)
