import logging
from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QVBoxLayout

from sknrf.model.base import AbstractModel
from sknrf.view.base import AbstractView
from sknrf.view.desktop.sequencer.menu import SequencerView
from sknrf.view.desktop.sequencer.widgets import SequencerState
from sknrf.view.desktop.sideview.sequencer import SequencerSideView
from sknrf.view.desktop.sideview.calkit import CalkitSideView
from sknrf.view.desktop.transform.circuit import TransformSideView
from sknrf.view.desktop.sideview.base import LogSideView
from sknrf.view.desktop.preview.frame import SignalPreviewFrame

__author__ = 'dtbespal'


logger = logging.getLogger(__name__)


class CalibrationView(SequencerView):

    def __init__(self, device_model, datagroup_model, package_map, parent=None, model=None, base_class=AbstractView):
        super(CalibrationView, self).__init__(device_model, datagroup_model, package_map, parent=parent, model=model, base_class=base_class)
        self.setWindowTitle("Calibration Menu")
        self.separate_thread = False
        log_side_view = LogSideView(AbstractModel, logger, parent=self.sideViewTabWidget)

        # Initialize Views
        self.sideViewTabWidget.clear()
        self.sidebar_views = OrderedDict(
            (("Sequencer", SequencerSideView(model=package_map, parent=self.sideViewTabWidget,
                                             base_class=AbstractView, enable_methods=False)),
             ("Calkits", CalkitSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
             ("Transforms", TransformSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
             ("Log", log_side_view)))
        for tab_name, tab_widget in self.sidebar_views.items():
            self.sideViewTabWidget.addTab(tab_widget, tab_name)

        self.toolBar.removeAction(self.actionCode)
        self.toolBar.removeAction(self.actionCompile)
        self.toolBar.removeAction(self.actionStep)
        self.toolBar.removeAction(self.actionStop)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/PNG/black/32/circled_border_triangle_right.png"),
                       QIcon.Normal, QIcon.Off)
        self.actionRun.setIcon(icon)
        self.actionRun.setCheckable(False)

        self.sequencerFrame.sequenceLabel.hide()
        self.sequencerFrame.sequenceTreeView.hide()

        self.sequencerFrame.previewTabWidget.clear()
        self.sequencerFrame.signalsTab = QWidget()
        self.sequencerFrame.signalsTab.setObjectName("signalsTab")
        self.sequencerFrame.signal_preview_frame = SignalPreviewFrame(parent=self.sequencerFrame.signalsTab)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.sequencerFrame.signal_preview_frame)
        self.sequencerFrame.signalsTab.setLayout(layout)
        self.sequencerFrame.previewTabWidget.addTab(self.sequencerFrame.signalsTab, "Signals")

    def disconnect_signals(self):
        self.sequencerFrame.disconnect_signals()

        self.actionNew.triggered.disconnect()
        self.actionLoad.triggered.disconnect()
        self.actionSave.triggered.disconnect()
        self.actionSave_As.triggered.disconnect()

        self.actionDocumentation.triggered.disconnect()

        self.actionCode.triggered.disconnect()
        self.actionCompile.triggered.disconnect()

        self.actionStep.triggered.disconnect()
        self.actionRun.triggered.disconnect()
        self.actionStop.triggered.disconnect()

        self.sequencerFrame.importListView.model().rowsInserted.disconnect()
        self.sequencerFrame.variableTableWidget.action_model().rowsInserted.disconnect()
        self.sequencerFrame.sequenceTreeView.model().rowsInserted.disconnect()
        self.sequencerFrame.importListView.model().dataChanged.disconnect()
        self.sequencerFrame.variableTableWidget.action_model().dataChanged.disconnect()
        self.sequencerFrame.sequenceTreeView.model().dataChanged.disconnect()
        self.sequencerFrame.importListView.model().rowsRemoved.disconnect()
        self.sequencerFrame.variableTableWidget.action_model().rowsRemoved.disconnect()
        self.sequencerFrame.sequenceTreeView.model().rowsRemoved.disconnect()

    def updateMicroFocus(self, *args, **kwargs):
        super().updateMicroFocus(*args, **kwargs)

    def setEnabled(self, enable):
        super(CalibrationView, self).setEnabled(enable)
        if SequencerState.variable:
            self.actionRun.setEnabled(True)

    @QtCore.Slot(bool)
    def run(self, checked=False):
        current_variable = SequencerState.variable
        current_variable.restart()
        current_variable.accepted.connect(self.update)
        current_variable.show()
