from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QWidget, QLabel, QSlider
from PySide2.QtWidgets import QGridLayout

from sknrf.utilities.numeric import num2str


class SweepSlider(QSlider):
    def wheelEvent(self, event):
        event.ignore()


class SweepSliderWidget(QWidget):

    def __init__(self, name, value, info, parent):
        self._parent = parent
        self.info = info
        super(SweepSliderWidget, self).__init__(parent)
        self.gbl = QGridLayout()
        self.name_label = QLabel(name)
        self.min_label = QLabel(num2str(info.min, info=info))
        self.max_label = QLabel(num2str(info.max, info=info))
        self.slider = SweepSlider()

        self.gbl.setContentsMargins(0, 0, 0, 0)
        self.gbl.setSpacing(0)
        self.min_label.setMaximumSize(QSize(16777215, 20))
        self.gbl.addWidget(self.min_label, 0, 0, 1, 1)
        self.name_label.setMaximumSize(QSize(16777215, 20))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.gbl.addWidget(self.name_label, 0, 1, 1, 1)
        self.max_label.setMaximumSize(QSize(16777215, 20))
        self.max_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gbl.addWidget(self.max_label, 0, 2, 1, 1)
        self.slider.setMinimum(info.min*10**info.precision)
        self.slider.setMaximum(info.max*10**info.precision)
        self.slider.setSingleStep(info.step*10**info.precision)
        self.slider.setPageStep(info.step*10**(info.precision+1))
        self.slider.setTracking(False)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.set_value(value)
        self.gbl.addWidget(self.slider, 1, 0, 1, 3)
        self.setLayout(self.gbl)

    def value(self):
        return self.slider.value()/10**self.info.precision

    def set_value(self, value):
        self.slider.setValue(value*10**self.info.precision)

    def minimum(self):
        return self.slider.minimum()/10**self.info.precision

    def set_minimum(self, value):
        self.slider.setMinimum(value*10**self.info.precision)
        self.min_label.setText(num2str(self.info.min, info=self.info))

    def maximum(self):
        return self.slider.maximum()/10**self.info.precision

    def set_maximum(self, value):
        self.slider.setMaximum(value*10**self.info.precision)
        self.max_label.setText(num2str(self.info.max, info=self.info))

    def update(self, value, info, labels=False, slider=False):
        super(SweepSliderWidget, self).update()
        all_ = not (labels and slider)
        self.info = info

        if labels or all_:
            self.set_minimum(self.info.min)
            self.set_maximum(self.info.max)

        if slider or all_:
            self.set_value(value)
