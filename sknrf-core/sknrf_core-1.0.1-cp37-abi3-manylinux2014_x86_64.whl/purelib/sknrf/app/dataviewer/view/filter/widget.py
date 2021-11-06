import abc
import logging

import numpy as np
import skrf
from PySide2 import QtCore
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QFrame, QWidget, QMessageBox, QLabel, QComboBox, QSlider
from PySide2.QtWidgets import QGridLayout, QVBoxLayout, QSizePolicy
from matplotlib import path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.collections import RegularPolyCollection
from matplotlib.colors import colorConverter
from matplotlib.figure import Figure
from matplotlib.projections.polar import InvertedPolarTransform
from matplotlib.widgets import Lasso

from sknrf.widget.rangeslider.view import QRangeSlider
from sknrf.utilities.rf import t2n

logger = logging.getLogger()


class Datum(object):
    """Data point container that adds color information.

        Parameters
        ----------
        x : float
            x-coordinate.
        y : float
            y-coordinate.
        color : RGB
            point color.
    """
    colorin = colorConverter.to_rgba('red')
    colorShift = colorConverter.to_rgba('cyan')
    colorCtrl = colorConverter.to_rgba('pink')
    colorout = colorConverter.to_rgba('blue')

    def __init__(self, x, y, include_=True):
        self.x = x
        self.y = y
        if include_:
            self.color = self.colorin
        else:
            self.color = self.colorout


class LassoManager(QWidget):
    """Interactive Lasso for selecting data points.

        Parameters
        ----------
        ax : matplotlib.axes
            current axes.
        data : list
            list of Datum points.
        transform : matplotlib.Transform, optional
            projection transform to apply to data input
    """

    selection_changed = QtCore.Signal(object)

    def __init__(self, ax, data, transform=None):
        super(LassoManager, self).__init__()
        self.axes = ax
        self.canvas = ax.figure.canvas
        self.data = data
        self._transform = transform

        self.Nxy = len(data)

        facecolors = [d.color for d in data]
        self.xys = [(d.x, d.y) for d in data]
        self.xys = self._transform.transform(self.xys) if self._transform else self.xys
        fig = ax.figure
        self.collection = RegularPolyCollection(int(fig.dpi), 6, sizes=(100,), facecolors=facecolors, offsets=self.xys,
                                                transOffset=ax.transData)

        ax.add_collection(self.collection)

        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.keyPress = self.canvas.mpl_connect('key_press_event', self.onKeyPress)
        self.keyRelease = self.canvas.mpl_connect('key_release_event', self.onKeyRelease)
        self.pick = self.canvas.mpl_connect('pick_event', self.onpick)
        self.lasso = None
        self.shiftKey = False
        self.ctrlKey = False
        self.pickEvent = False

    def callback(self, verts):
        """Updates the facecolors and emits the selection_changed signal containing the lassoed points.

        Parameters
        ----------
        verts : ndarray
            vertices of the lasso trace.
        """
        logging.debug('in LassoManager.callback(). Shift: %s, Ctrl: %s' % (self.shiftKey, self.ctrlKey))
        facecolors = self.collection.get_facecolors()
        p = path.Path(verts)
        ind = p.contains_points(self.xys)
        if np.any(ind):
            for i in range(len(self.xys)):
                if ind[i]:
                    if self.shiftKey:
                        facecolors[i] = Datum.colorShift
                    elif self.ctrlKey:
                        facecolors[i] = Datum.colorCtrl
                    else:
                        facecolors[i] = Datum.colorin
                else:
                    facecolors[i] = Datum.colorout
            self.canvas.draw_idle()
            self.canvas.widgetlock.release(self.lasso)
            del self.lasso
            self.selection_changed.emit(ind)
        else:
            warning_message = "At least one point must be selected."
            logger.warning(warning_message)
            QMessageBox.warning(self,
                                      self.tr("DataViewer"),
                                      self.tr(warning_message),
                                      QMessageBox.Ok | QMessageBox.Ok,
                                      QMessageBox.Ok)
            self.canvas.draw_idle()
            self.canvas.widgetlock.release(self.lasso)
            del self.lasso

    def onpress(self, event):
        """Callback for mouse button press

            Parameters
            ----------
            event : matplotlib.event
                a callback event.
        """
        logging.debug('in LassoManager.onpress(). Event received: %s' % event)
        if self.pickEvent:
            self.pickEvent = False
            return
        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)

    def onKeyPress(self, event):
        """Callback for keyboard button press

            Parameters
            ----------
            event : matplotlib.event
                a callback event.
        """
        logging.debug('in LassoManager.onKeyPress(). Event received: %s (key: %s)' % (event, event.key))
        if event.key == 'alt':
            self.ctrlKey = True
        if event.key == 'shift':
            self.shiftKey = True

    def onKeyRelease(self, event):
        """Callback for keyboard button release

            Parameters
            ----------
            event : matplotlib.event
                a callback event.
        """
        logging.debug('in LassoManager.onKeyRelease(). Event received: %s (key: %s)' % (event, event.key))
        if event.key == 'alt':
            self.ctrlKey = False
        if event.key == 'shift':
            self.shiftKey = False

    def onpick(self, event):
        """Callback for keyboard button release

            Parameters
            ----------
            event : matplotlib.event
                a callback event.
        """
        logging.debug('in LassoManager.onpick(). Event received: %s' % event)
        self.pickEvent = True
        # if event.mouseevent.button == 3:
        #     index = event.ind
        #     print('onpick scatter: ' + index + np.take(x, index) + np.take(y, index))


class AbstractFilter(QFrame):
    """Abstract Filter.

        Attributes
        ----------
        filter_changed : QtCore.Signal
            signal emitted when filter is changed.
    """
    filter_changed = QtCore.Signal()

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super(AbstractFilter, self).__init__(*args, **kwargs)


class RealFilter(AbstractFilter):

    def __init__(self, name, values, parent):
        self._parent = parent
        super(RealFilter, self).__init__(parent)
        self.gbl = QGridLayout()
        self.type = ""  # (Point, Range)
        self.name_label = QLabel(name)
        self.value = np.unique(values)
        self.min_label = QLabel("0")
        self.max_label = QLabel("1")
        self.slider = QRangeSlider()

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
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.value.size-1)
        self.slider.setPageStep(self.value.size-1)
        self.slider.setSpan(0, self.value.size-1)
        self.slider.setTracking(False)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(1)
        if name != 'time':
            self.slider.setHandleMovementMode(QRangeSlider.NoCrossing)
        else:
            self.slider.setHandleMovementMode(QRangeSlider.NoOverlapping)
        self.connect_signals()
        self.set_min_label(0)
        self.set_max_label(self.value.size-1)
        self.gbl.addWidget(self.slider, 1, 0, 1, 3)
        self.setLayout(self.gbl)

    def connect_signals(self):
        self.slider.lowerPositionChanged.connect(self.set_min_label)
        self.slider.lowerValueChanged.connect(self.set_lower_index)
        self.slider.upperPositionChanged.connect(self.set_max_label)
        self.slider.upperValueChanged.connect(self.set_upper_index)

    def disconnect_signals(self):
        self.slider.lowerPositionChanged.disconnect()
        self.slider.lowerValueChanged.disconnect()
        self.slider.upperPositionChanged.disconnect()
        self.slider.upperValueChanged.disconnect()

    def lower_index(self):
        return self.slider.lowerValue()

    def set_lower_index(self, index):
        self.slider.setLowerValue(index)
        self.set_min_label(index)
        self.filter_changed.emit()

    def upper_index(self):
        return self.slider.upperValue()

    def set_upper_index(self, index):
        self.slider.setUpperValue(index)
        self.set_max_label(index)
        self.filter_changed.emit()

    def lower_value(self):
        index = self.slider.lowerValue()
        return self.value[index]

    def upper_value(self):
        index = self.slider.upperValue()
        return self.value[index]

    def set_min_label(self, index):
        self.min_label.setText(str(self.value[index]))

    def set_max_label(self, index):
        self.max_label.setText(str(self.value[index]))
        

class ComplexFilter(AbstractFilter):
    """Complex Filter.

        Contains an interactive plot to limit the range of an arbitrary complex number sweep. The following formats are
        supported:

            * Rectangular plot
            * Polar plot
            * Smith Chart plot

        Attributes
        ----------
        figure : matplotlib.figure
            the figure.
        canvas : matplotlib.canvas
            the canvas
        axes : matplotlib.axes
            the axes.
        ind : array_like
            a boolean array, True if the index is selected, False if the index is deselected.
    """
    def __init__(self, name, values, parent=None):
        super(ComplexFilter, self).__init__(parent)
        self._name = name
        self._values = values
        self.setupUi(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.gca()
        self._lasso_manager = None
        self.ind = []

        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.set_axes("Rectangular")
        self.connect_signals()

    def setupUi(self, ComplexFilter):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        self.comboBox = QComboBox(self)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Rectangular")
        self.comboBox.addItem("Polar")
        self.comboBox.addItem("Smith")

    def connect_signals(self):
        self.comboBox.currentIndexChanged[str].connect(self.set_axes)

    def disconnect_signals(self):
        self.comboBox.currentIndexChanged[str].disconnect(self.set_axes)

    def heightForWidth(self, width):
        return width*1.0

    def sizeHint(self):
        return QSize(400, 400)

    @QtCore.Slot(str)
    def set_axes(self, format_):
        """Set the axes to the format provided.

            Parameters
            ----------
            format_ : str
                The plot format.
        """
        self.figure.clear()
        data = self._values
        if format_ == "Rectangular":
            transform = None
            x, y = data.real, data.imag
            self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
            self.axes.set_xlim(left=np.minimum(np.sqrt(1.1)*np.min(x), -0.01),
                               right=np.maximum(np.sqrt(1.1)*np.max(x), 0.01))
            self.axes.set_ylim(bottom=np.minimum(np.sqrt(1.1)*np.min(y), -0.01),
                               top=np.maximum(np.sqrt(1.1)*np.max(y), 0.01))
        elif format_ == "Polar":
            transform = InvertedPolarTransform()
            x, y = data.real, data.imag
            _data = transform.inverted().transform((data.real, data.imag))
            self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8], projection="polar")
            self.axes.set_rmax(1.1*np.max(np.abs(data)))
        elif format_ == "Smith":
            transform = None
            x, y = data.real, data.imag
            self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
            skrf.plotting.smith(ax=self.axes)
        else:
            raise ValueError("Unknown Axes Type: %s" % (format_,))
        self.axes.grid(True)
        data = [Datum(*xy) for xy in zip(x, y)]
        self._lasso_manager = LassoManager(self.axes, data, transform=transform)
        self._lasso_manager.selection_changed.connect(self.set_selection)
        self.update()

    @QtCore.Slot(object)
    def set_selection(self, ind):
        self.ind = ind
        self.filter_changed.emit()

    def update(self):
        self.figure.canvas.draw()
