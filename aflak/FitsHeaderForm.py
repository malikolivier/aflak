from pyqtgraph.Qt import QtWidgets

from .FitsHeaderForm_ui import Ui_Form


class FitsHeaderForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def setHdu(self, hdu):
        self.ui.plainTextEdit.setPlainText(repr(hdu.header))
