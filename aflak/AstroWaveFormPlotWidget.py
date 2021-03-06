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
        unit = self.fitsFile.wave_unit()
        if unit is not None:
            text = 'Wavelength (%s)' % unit
        else:
            text = 'Wavelength'
        self.setLabel('bottom', text=text)

    def updateAstroDisplay(self, show):
        if show and self.fitsFile is not None:
            unit = self.fitsFile.summed_flux_unit()
            if unit:
                text = 'Flux ({})'.format(unit)
            else:
                text = 'Flux'
            self.setLabel('left', text=text)
        else:
            self.showLabel('left', show=False)
