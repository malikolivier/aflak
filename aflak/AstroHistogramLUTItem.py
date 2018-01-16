from pyqtgraph.graphicsItems.HistogramLUTItem import HistogramLUTItem


class AstroHistogramLUTItem(HistogramLUTItem):
    """
    Extends default HistogramLUTItem.
    - Histogram's y coordinates are shown using a logarithmic scale
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plot.setLogMode(False, True)
