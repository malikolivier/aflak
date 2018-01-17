from pyqtgraph.graphicsItems.HistogramLUTItem import HistogramLUTItem
from pyqtgraph.graphicsItems.AxisItem import AxisItem


class AstroHistogramLUTAxisItem(AxisItem):
    pass


class AstroHistogramLUTItem(HistogramLUTItem):
    """
    Extends default HistogramLUTItem.
    - Histogram's y coordinates are shown using a logarithmic scale
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plot.setLogMode(False, True)
        self.yAxis = AstroHistogramLUTAxisItem('bottom', linkView=self.vb, parent=self)
        self.yAxis.setLabel(text="Flux", unit="UNIT")
        print(self.yAxis.labelString())
        print(self.vb.sigYRangeChanged)
        self.layout.addItem(self.yAxis, 3, 1)
