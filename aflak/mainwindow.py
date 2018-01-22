from pyqtgraph.Qt import QtGui, QtWidgets

from .mainwindow_ui import Ui_MainWindow
from .AboutDialog import AboutDialog
from .AstroImageView import AstroImageView
from .FitsHeaderWindow import FitsHeaderWindow
from .MultiROI import ROIType

from .fits import FITS
from .settings import Settings


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.astroImageView)

        # QtDesigner does not support QActionGroup (radio button), so we handle
        # it outside of the generated UI file
        self.roiSelectGroup = QtWidgets.QActionGroup(self)
        self.roiSelectGroup.addAction(self.ui.actionDisable_ROI)
        self.roiSelectGroup.addAction(self.ui.actionRectangular_ROI)
        self.roiSelectGroup.addAction(self.ui.actionPolygonal_ROI)
        self.roiSelectGroup.addAction(self.ui.actionElliptic_ROI)
        self.roiSelectGroup.addAction(self.ui.actionSemi_automatic_ROI)

        # Populate "Recent Files" menu
        recentFiles = Settings.getRecentFiles()
        for i, path in enumerate(recentFiles):
            if i == 0:
                self.ui.action_NoRecentFile.setVisible(False)
            recentFileAction = QtWidgets.QAction(self)
            recentFileAction.setText("%i | %s" % (i, path))
            openFileFunction = self._createOpenFileFunction(path)
            recentFileAction.triggered.connect(openFileFunction)
            self.ui.menuRecent_Files.insertAction(self.ui.actionClear_Menu,
                                                  recentFileAction)
            if i == len(recentFiles) - 1:
                self.ui.menuRecent_Files.insertSeparator(
                    self.ui.actionClear_Menu)

        # Connect actions to event handlers
        self.ui.actionExit.triggered.connect(QtWidgets.qApp.quit)
        self.ui.actionOpen.triggered.connect(self._open_file)
        self.ui.actionClear_Menu.triggered.connect(self._clearRecentFiles)
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
        Settings.addRecentFile(file_path)
        self.setWindowTitle('aflak - %s' % file_path)
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

    def _createOpenFileFunction(self, path):
        def openFile():
            self.set_fits_file(path)
        return openFile

    def _clearRecentFiles(self):
        Settings.clearRecentFiles()
        self.ui.action_NoRecentFile.setVisible(True)
        for action in self.ui.menuRecent_Files.actions():
            if (action is not self.ui.action_NoRecentFile and
                    action is not self.ui.actionClear_Menu):
                self.ui.menuRecent_Files.removeAction(action)

    def _openFitsHeaderDialog(self):
        self.dialog = FitsHeaderWindow(self.fitsFile)
        self.dialog.show()

    def _selectROI(self, selectedAction):
        name = selectedAction.objectName()
        if name == 'actionDisable_ROI':
            self.ui.astroImageView.setROIType(None)
        elif name == 'actionElliptic_ROI':
            self.ui.astroImageView.setROIType(ROIType.ELLIPSE)
        elif name == 'actionPolygonal_ROI':
            self.ui.astroImageView.setROIType(ROIType.POLYGON)
        elif name == 'actionRectangular_ROI':
            self.ui.astroImageView.setROIType(ROIType.RECTANGLE)
        elif name == 'actionSemi_automatic_ROI':
            self.ui.astroImageView.setROIType(ROIType.SEMIAUTOMATIC)
        else:
            raise NotImplementedError('Unknown action name: %s' % name)

    def _openAboutDialog(self):
        AboutDialog().exec_()
