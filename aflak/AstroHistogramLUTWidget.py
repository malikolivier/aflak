from pyqtgraph.Qt import QtGui
from pyqtgraph.widgets.HistogramLUTWidget import HistogramLUTWidget
from pyqtgraph.widgets.GraphicsView import GraphicsView

from .AstroHistogramLUTItem import AstroHistogramLUTItem


class AstroHistogramLUTWidget(HistogramLUTWidget):
    """
    Extends HistogramLUTWidget to use AstroHistogramLUTItem instead of
    the default HistogramLUTItem
    """
    def __init__(self, parent=None,  *args, **kargs):
        background = kargs.get('background', 'default')
        GraphicsView.__init__(self, parent, useOpenGL=False,
                              background=background)
        self.item = AstroHistogramLUTItem(*args, **kargs)
        self.setCentralItem(self.item)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,
                           QtGui.QSizePolicy.Expanding)
        self.setMinimumWidth(95)
