from pyqtgraph.Qt import QtGui, QtWidgets

from .mainwindow_ui import Ui_MainWindow
from .AboutDialog import AboutDialog
from .AstroImageView import AstroImageView
from .FitsHeaderWindow import FitsHeaderWindow
from .MultiROI import ROIType

from .fits import FITS


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.astroImageView)

        # QtDesigner does not support QActionGroup (radio button), so we handle
        # it outside of the generated UI file
        self.roiSelectGroup = QtWidgets.QActionGroup(self)
        self.roiSelectGroup.addAction(self.ui.actionRectangular_ROI)
        self.roiSelectGroup.addAction(self.ui.actionPolygonal_ROI)
        self.roiSelectGroup.addAction(self.ui.actionElliptic_ROI)

        self.ui.actionExit.triggered.connect(QtWidgets.qApp.quit)
        self.ui.actionOpen.triggered.connect(self._open_file)
        self.ui.actionSee_FITS_header.triggered.connect(
            self._openFitsHeaderDialog
        )
        self.roiSelectGroup.triggered.connect(self._selectROI)
        self.ui.actionAbout.triggered.connect(self._openAboutDialog)

        self.fitsFileStatusBarLabel = QtGui.QLabel()
        self.ui.statusbar.addPermanentWidget(self.fitsFileStatusBarLabel)
        self.dialog = None
        self.fitsFile = None

    def set_fits_file(self, file_path):
        self.setWindowTitle(file_path)
        self.fitsFile = FITS(file_path)
        self.ui.astroImageView.set_fits_file(self.fitsFile)
        self.ui.menuFITS.setEnabled(True)
        self.fitsFileStatusBarLabel.setText(file_path)

    def _open_file(self):
        name, _file_type = QtGui.QFileDialog.getOpenFileName(self,
                                                             'Open File')
        # `name' is an empty string if the user pressed `Cancel' in the
        # open-file dialog
        if name != '':
            self.set_fits_file(name)

    def _openFitsHeaderDialog(self):
        self.dialog = FitsHeaderWindow(self.fitsFile)
        self.dialog.show()

    def _selectROI(self, selectedAction):
        name = selectedAction.objectName()
        if name == 'actionElliptic_ROI':
            self.ui.astroImageView.setROIType(ROIType.ELLIPSE)
        elif name == 'actionPolygonal_ROI':
            self.ui.astroImageView.setROIType(ROIType.POLYGON)
        elif name == 'actionRectangular_ROI':
            self.ui.astroImageView.setROIType(ROIType.RECTANGLE)
        else:
            raise NotImplementedError('Unknown action name: %s' % name)

    def _openAboutDialog(self):
        AboutDialog().exec_()
