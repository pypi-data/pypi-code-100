import abc
import logging

from PySide2 import QtCore
from PySide2.QtCore import QSize
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QFrame, QTabWidget, QLabel, QProgressBar, QSpacerItem
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy
import numpy as np

from sknrf.settings import Settings
from sknrf.view.base import AbstractView
from sknrf.view.desktop.sideview.QLogSideView import Ui_logFrame
from sknrf.view.desktop.sideview.QProgressSideView import Ui_progressFrame
from sknrf.utilities.numeric import unravel_index


class AbstractSideView(AbstractView):
    update_main_window = QtCore.Signal()

    def __init__(self, parent=None):
        self._parent = parent
        super(AbstractSideView, self).__init__(parent=parent)

    def update_window(self):
        self.update_main_window.emit()

    def update(self, *args):
        super(AbstractSideView, self).update()


class LogSideView(AbstractSideView, QFrame, Ui_logFrame):

    def __init__(self, model, logger, parent=None):
        super(LogSideView, self).__init__(parent=parent)
        self.setupUi(self)
        self.level_color_map = {"DEBUG": Settings().color_map["black"],
                                "INFO": Settings().color_map["green"],
                                "WARNING": Settings().color_map["yellow"],
                                "ERROR": Settings().color_map["red"],
                                "CRITICAL": Settings().color_map["magenta"]}
        self._logger = None
        self._handler = None
        self._formatter = None
        self.connect_signals()
        self.set_logger(logger)

    def connect_signals(self):
        if self._handler:
            self._handler.q_object.new_record.connect(self.add_record)
        self.levelComboBox.currentIndexChanged.connect(self.set_level)

    def disconnect_signals(self):
        if self._handler:
            self._handler.q_object.new_record.disconnect()
        self.levelComboBox.currentIndexChanged.disconnect()

    def logger(self):
        return self._logger.level

    def set_logger(self, logger):
        self.disconnect_signals()
        self._logger = logger
        self._handler = Settings()._qt_logging_handler
        self._formatter = logging.Formatter('%(asctime)s - %(name)s')
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)
        self.set_level(self.level())
        self.connect_signals()

    def level(self):
        return max(self._handler.level / 10 - 1, 0)

    def set_level(self, level):
        self._handler.setLevel(int((level + 1) * 10))
        self._logger.setLevel(int((level + 1) * 10))
        self.levelComboBox.setCurrentIndex(level)

    def add_record(self, record):
        record_str = self._handler.format(record)
        self.textEdit.setTextColor(QColor(self.level_color_map[record.levelname]))
        self.textEdit.setFontWeight(600)
        self.textEdit.append(record_str)
        self.textEdit.setFontWeight(400)
        self.textEdit.append(record.getMessage())


class ProgressSideView(AbstractSideView, QFrame, Ui_progressFrame):
    """Progress Update runtime status.

    The progress update frame contains the following information:
        * The sequencer status.
        * The parametric sweep status.
        * The optimization status.

        Keyword Args:
            datagroup (DatagroupModel): The Datagroup where measurements are being saved.
            parent (QWidget): Parent GUI container.
    """
    def __init__(self, model, parent=None):
        super(ProgressSideView, self).__init__(parent=parent)
        self.setupUi(self)

        self.sweep_vbl = QVBoxLayout(self.scrollAreaWidgetContents)
        self.progress_labels = []
        self.progress_bars = []
        self.sweep_shape = np.ones(1, dtype=int)
        devices = model.device_model()
        self.offset = devices.sweep_step()*devices.step()

        self.set_model(model)

    def set_dataset(self, datagroup_name, dataset_name):
        for child in self.sweep_vbl.children():
            child.deleteLater()
        ds = self._model.datagroup_model()[datagroup_name].dataset(dataset_name)
        sweep_names = list(ds.sweep_map.keys())
        self.progress_labels = [None]*len(sweep_names)
        self.progress_bars = [None]*len(sweep_names)
        self.sweep_shape = ds.shape
        for ind in range(len(sweep_names)):
            sweep_name = sweep_names[ind]
            self.progress_labels[ind] = QLabel(sweep_name)
            self.progress_bars[ind] = QProgressBar(self.scrollAreaWidgetContents)
            self.progress_bars[ind].setMinimum(0)
            self.progress_bars[ind].setMaximum(self.sweep_shape[-ind-1]-1)
            self.progress_bars[ind].setValue(0)
            self.sweep_vbl.addWidget(self.progress_labels[ind])
            self.sweep_vbl.addWidget(self.progress_bars[ind])
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sweep_vbl.addItem(spacer_item)

    def update(self, batch_index, *args):
        # todo: use th.unravel_index (See Pytorch #35674)
        array_index = unravel_index(batch_index * self.offset, self.sweep_shape) if batch_index > -1 else \
                      np.asarray(self.sweep_shape) - 1

        ind = 0
        for progress_bar in self.progress_bars:
            progress_bar.setValue(array_index[-ind-1])
            ind += 1


class SideViewTabWidget(QTabWidget):
    """Reconfigurable sideview GUI for custom GUI control modules

        Keyword Args:
            parent (QWidget): Parent GUI container
    """
    def __init__(self, parent=None):
        super(SideViewTabWidget, self).__init__(parent)

        # Sidebar
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QSize(300, 0))
        self.setTabPosition(QTabWidget.West)
        self.setObjectName("sideViewWidget")

        self.connect_signals()

    def connect_signals(self):
        self.currentChanged.connect(self.update)

    def disconnect_signals(self):
        self.currentChanged.disconnect(self.update)

    def sizeHint(self):
        return QSize(300, 300)

    def update(self, *args):
        current_widget = self.currentWidget()
        if current_widget and current_widget.model():
            current_widget.update(*args)
