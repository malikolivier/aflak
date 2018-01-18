from pyqtgraph.widgets.PlotWidget import PlotWidget


class AstroWaveFormPlotWidget(PlotWidget):
    """
    Extends PlotWidget.
     - Add units and labels to plot
     - Flux unit is directly read from FITS file
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fitsFile = None

    def setFitsFile(self, fits):
        self.fitsFile = fits
        self.setLabel('bottom', text='Wavelength', units='Å')

    def updateAstroDisplay(self, show):
        if show and self.fitsFile is not None:
            unit = self.fitsFile.summed_flux_unit()
            self.setLabel('left', text='Flux ({})'.format(unit))
        else:
            self.showLabel('left', show=False)
