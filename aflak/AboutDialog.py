from pyqtgraph.Qt import QtWidgets

from . import __version__
from .AboutDialog_ui import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog):
        def __init__(self):
            super().__init__()
            self.ui = Ui_AboutDialog()
            self.ui.setupUi(self)
            self.ui.closeButton.clicked.connect(self.close)
            self.ui.versionLabel.setText(__version__)
