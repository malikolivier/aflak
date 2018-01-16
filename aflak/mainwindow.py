from pyqtgraph.Qt import QtGui, QtWidgets

from .mainwindow_ui import Ui_MainWindow
from .viewer import AstroImageViewer


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionExit.triggered.connect(QtWidgets.qApp.quit)
        self.ui.actionOpen.triggered.connect(self._open_file)

        self.viewer = AstroImageViewer()
        self.setCentralWidget(self.viewer.imv)
        self.show()

    def set_fits_file(self, file_path):
        self.setWindowTitle(file_path)
        self.viewer.set_fits_file(file_path)

    def _open_file(self):
        name, _file_type = QtGui.QFileDialog.getOpenFileName(self,
                                                             'Open File')
        # `name' is an empty string if the user pressed `Cancel' in the
        # open-file dialog
        if name != '':
            self.set_fits_file(name)
