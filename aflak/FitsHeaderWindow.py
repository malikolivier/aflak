from pyqtgraph.Qt import QtWidgets

from .FitsHeaderWindow_ui import Ui_FitsHeaderWindow


class FitsHeaderWindow(QtWidgets.QDialog):
    def __init__(self, fitsFile):
        super().__init__()
        self.ui = Ui_FitsHeaderWindow()
        self.ui.setupUi(self)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.fileNameField.setText(fitsFile.name)
