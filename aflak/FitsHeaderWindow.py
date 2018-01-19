from pyqtgraph.Qt import QtWidgets

from .FitsHeaderForm import FitsHeaderForm
from .FitsHeaderWindow_ui import Ui_FitsHeaderWindow


class FitsHeaderWindow(QtWidgets.QDialog):
    def __init__(self, fitsFile):
        super().__init__()
        self.ui = Ui_FitsHeaderWindow()
        self.ui.setupUi(self)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.fileNameField.setText(fitsFile.name)
        for i, hdu in enumerate(fitsFile.hdulist):
            tab = QtWidgets.QWidget()
            gridLayout = QtWidgets.QGridLayout(tab)
            tabContent = FitsHeaderForm(tab)
            tabContent.setHdu(hdu)
            gridLayout.addWidget(tabContent)
            self.ui.tabWidget.addTab(tab, "")
            self.ui.tabWidget.setTabText(
                self.ui.tabWidget.indexOf(tab), "[%d] %s" % (i, hdu.name)
            )
