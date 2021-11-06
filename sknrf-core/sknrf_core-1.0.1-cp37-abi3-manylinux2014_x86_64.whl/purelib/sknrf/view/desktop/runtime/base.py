import os
from collections import OrderedDict
import logging
import time

from PySide2 import QtCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QMainWindow, QFrame, QWidget, QSplitter, QMessageBox
from PySide2.QtWidgets import QHBoxLayout, QSizePolicy

from sknrf.settings import Settings
from sknrf.enums.runtime import RuntimeState
from sknrf.model.base import AbstractModel
from sknrf.view.desktop.sideview.base import SideViewTabWidget, ProgressSideView, LogSideView
from sknrf.view.desktop.runtime.QRuntime import Ui_runtime


logger = logging.getLogger(__name__)

__author__ = 'dtbespal'


class AbstractRuntimeView(QMainWindow, Ui_runtime):
    """The base runtime window

    A runtime window that contains:
        * A ProgressUpdateView.

        Keyword Args:
            parent (QWidget): Parent GUI container.
    """

    resume_request = QtCore.Signal()

    def __init__(self, parent=None):
        super(AbstractRuntimeView, self).__init__(parent)
        self.setupUi(self)
        self.stimulus_ports = [1, 2]
        self.ss_stimulus_ports = [1, 2]

        # Right Align Measurement Buttons of Toolbar
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionRun, empty)

        # Content Splitter
        self.splitter = QSplitter(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setSizePolicy(size_policy)
        self.splitter.setOrientation(Qt.Horizontal)

        self.sideViewTabWidget = SideViewTabWidget(parent=self.splitter)
        self.content_frame = QFrame(self.splitter)
        self.splitter.addWidget(self.sideViewTabWidget)
        self.splitter.addWidget(self.content_frame)
        self.layout = QHBoxLayout(self.centralwidget)
        self.layout.addWidget(self.splitter)
        self.hbl = QHBoxLayout(self.content_frame)
        self.splitter.setSizes([1, 1000])
        self.connect_signals()

    @QtCore.Slot(object)
    def initialize(self, model):
        self.sidebar_views = OrderedDict((("Progress", ProgressSideView(model=AbstractModel, parent=self.sideViewTabWidget)),))
                                          # ("Log", LogSideView(AbstractModel, logger, parent=self.sideViewTabWidget))))
        for tab_name, tab_widget in self.sidebar_views.items():
            self.sideViewTabWidget.addTab(tab_widget, tab_name)
        self.sidebar_views["Progress"].set_dataset(Settings().datagroup, Settings().dataset)
        self.sidebar_views["Progress"].offset = model.device_model().step()

        self.showMaximized()
        self.run()
        self.resume_request.emit()

    def connect_signals(self):
        self.actionRun.triggered.connect(self.run)
        self.actionSingle.triggered.connect(self.single)
        self.actionPause.triggered.connect(self.pause)
        self.actionStop.triggered.connect(self.stop)

    def disconnect_signals(self):
        self.actionRun.triggered.disconnect()
        self.actionSingle.triggered.disconnect()
        self.actionPause.triggered.disconnect()
        self.actionStop.triggered.disconnect()

    def update(self, model=None, batch_index=-1, sideview=False, value=False):
        all_ = not (sideview or value)

        if sideview or all_:
            current_tab = self.sideViewTabWidget.currentWidget()
            if current_tab is self.sidebar_views["Progress"]:
                self.sidebar_views["Progress"].update(batch_index)
            else:
                current_tab.update(batch_index)

        state = Settings().runtime_state
        self.actionRun.setChecked(state == RuntimeState.RUN)
        self.actionSingle.setChecked(state == RuntimeState.SINGLE)
        self.actionPause.setChecked(state == RuntimeState.PAUSED)
        self.actionStop.setChecked(state == RuntimeState.STOPPED)
        self.actionRun.setEnabled(state == RuntimeState.PAUSED or state == RuntimeState.STOPPED)
        self.actionSingle.setEnabled(state == RuntimeState.PAUSED or state == RuntimeState.STOPPED)
        self.actionPause.setEnabled(state == RuntimeState.RUN)
        self.actionStop.setEnabled(state != RuntimeState.STOPPED)

        if model:
            self.resume_request.emit()

    @QtCore.Slot(object)
    def close(self, model):
        time.sleep(1)
        super(AbstractRuntimeView, self).close()
        self.resume_request.emit()

    @QtCore.Slot(bool)
    def run(self, checked=False):
        Settings().runtime_state = RuntimeState.RUN
        self.update()

    @QtCore.Slot(bool)
    def single(self, checked=False):
        Settings().runtime_state = RuntimeState.SINGLE
        self.update()

    @QtCore.Slot(bool)
    def pause(self, checked=False):
        Settings().runtime_state = RuntimeState.PAUSED
        self.update()

    @QtCore.Slot(bool)
    def stop(self, checked=False):
        Settings().runtime_state = RuntimeState.STOPPED
        self.update()

    def closeEvent(self, event):
        if Settings().runtime_state != RuntimeState.STOPPED:
            Settings().runtime_state = RuntimeState.STOPPED
            event.ignore()
            return
        super(AbstractRuntimeView, self).closeEvent(event)


if __name__ == "__main__":
    pass
