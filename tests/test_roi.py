from pyqtgraph.Qt import QtGui

from aflak.MultiROI import MultiROI, ROIType


def test_first_roi_is_rectangle():
    app = QtGui.QApplication([])
    roi = MultiROI()
    assert isinstance(roi.currentRoi, ROIType.RECTANGLE.value)
