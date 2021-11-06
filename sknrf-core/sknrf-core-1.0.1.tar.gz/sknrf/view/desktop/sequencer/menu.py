import os
import sys
import importlib
import pickle
import logging
from collections import OrderedDict

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QFrame, QWidget, QFileDialog, QMessageBox, QSplitter
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy
if sys.platform == "win32": import pythoncom

from sknrf.settings import Settings
from sknrf.enums.runtime import RuntimeState
from sknrf.model.base import AbstractModel
from sknrf.model.sequencer.base import ActionItemDataRole
from sknrf.model.sequencer.base import SequencerModel
from sknrf.view.base import AbstractView
from sknrf.view.desktop.sequencer.widgets import SequencerState
from sknrf.view.desktop.sequencer.code import CodeDialog
from sknrf.view.desktop.sequencer.QSequencerFrame import Ui_sequencerFrame
from sknrf.view.desktop.sequencer.QSequencerView import Ui_sequencerMenu
from sknrf.model.runtime import RuntimeThread, RuntimeModel
from sknrf.view.desktop.sideview.base import SideViewTabWidget, LogSideView
from sknrf.view.desktop.sideview.main import MainSideView
from sknrf.view.desktop.sideview.sequencer import SequencerSideView
from sknrf.view.desktop.preview.frame import SweepPreviewFrame, DatasetPreviewFrame
from sknrf.widget.propertybrowser.view.base import PropertyScrollArea
from sknrf.view.desktop.runtime.ls import LargeSignalRuntimeView

from sknrf.widget.propertybrowser.view import BrowserCol

__author__ = 'dtbespal'


logger = logging.getLogger(__name__)


class SequencerFrame(QFrame, Ui_sequencerFrame):
    """Sequencer Frame.
    """
    def __init__(self, device_model, datagroup_model, parent=None, model=None):
        super(SequencerFrame, self).__init__(parent)
        self.setupUi(self)

        self._model = None

        self.sweepsTab = QWidget()
        self.sweepsTab.setObjectName("sweepsTab")
        self.sweep_preview_frame = SweepPreviewFrame(parent=self.sweepsTab)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.sweep_preview_frame)
        self.sweepsTab.setLayout(layout)
        self.previewTabWidget.addTab(self.sweepsTab, "Sweeps")

        self.signalsTab = QWidget()
        self.signalsTab.setObjectName("signalsTab")
        self.signal_preview_frame = DatasetPreviewFrame(parent=self.signalsTab)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.signal_preview_frame)
        self.signalsTab.setLayout(layout)
        self.previewTabWidget.addTab(self.signalsTab, "Signals")

        if model is None:
            model = SequencerModel()
        self.set_model(model)
        self._base_variables = dict()
        self.sweep_preview_frame.set_model(self.variableTableWidget.model())
        if Settings().datagroup in self._model.datagroup_model():
            datagroup = datagroup_model[Settings().datagroup]
            if datagroup.has_dataset(Settings().dataset):
                dataset = datagroup.dataset(Settings().dataset)
                self.signal_preview_frame.set_model(dataset)

    def setEnabled(self, enable):
        """Controls the enabled state of widgets when switching between setup and debug mode.

        Args:
            enable (bool): enable is True for setup mode and false for debug mode.
        """
        super(SequencerFrame, self).setEnabled(enable)

    def model(self):
        return self._model

    def set_model(self, model):
        """Sets the model.

        Args:
            model (SequencerModel): The model.
        """
        self._model = model
        self.importListView.setModel(model.import_model())
        self.variableTableWidget.set_model(model.variable_model())
        self.sequenceTreeView.setModel(model.sequence_model())
        self.update()

    def connect_signals(self):
        self.variableTabWidget.currentChanged.connect(self.selected_property_tab)
        self.sweep_preview_frame.setting_changed.connect(self.update_variables)
        self.signal_preview_frame.setting_changed.connect(self.update_variables)

    def disconnect_signals(self):
        self.variableTabWidget.currentChanged.disconnect(self.selected_property_tab)
        self.sweep_preview_frame.setting_changed.disconnect(self.update_variables)
        self.signal_preview_frame.setting_changed.disconnect(self.update_variables)

    def clear(self):
        """Clears all ActionItems in the Import List, Variable Table, Sequence Tree, and Preview Tab Frame.
        """
        self.sweep_preview_frame.clear()
        self.signal_preview_frame.clear()
        self.model().sequence_model().clear()
        self.variableTableWidget.clear()
        self.model().import_model().clear()

    def selected_property_tab(self, _):
        """Updates the contents the Variable Table based on the tab selected.
        """
        self.disconnect_signals()
        tab = self.variableTabWidget.currentWidget()
        self.variableTableWidget.setParent(tab)
        self.variableTableWidget.show()
        self.variableTableWidget.clear()
        if tab == self.propertyTab:
            self.variableTableWidget.setAttributes([BrowserCol.UNIT, BrowserCol.PKAVG, BrowserCol.FORMAT])
        elif tab == self.limitTab:
            self.variableTableWidget.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.UNIT])
        elif tab == self.optimizationTab:
            self.variableTableWidget.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.UNIT])
        self.variableTableWidget.set_model(self._model.variable_model())
        self.connect_signals()

    def breakpoints(self):
        """Gets the breakpoint list.

        Return:
            breakpoints (list): A list of breakpoint line numbers.
        """
        return set(breakpoint + self.sequenceTreeView.breakpoint_offset
                   for breakpoint in self.sequenceTreeView.breakpoints())

    def set_breakpoints(self, breakpoints):
        """Sets the breakpoint list.

        Args:
            breakpoints (list): A list of breakpoint line numbers.
        """
        self.sequenceTreeView.set_breakpoints(set(breakpoint - self.sequenceTreeView.breakpoint_offset
                                                  for breakpoint in breakpoints))

    def active_breakpoint(self):
        """Gets the active breakpoint.

        Return:
            active_breakpoint (int): The active breakpoint line number.
        """
        return self.sequenceTreeView.active_breakpoint() + self.sequenceTreeView.breakpoint_offset

    def set_active_breakpoint(self, active_breakpoint):
        """Sets the active breakpoint.

        Return:
            active_breakpoint (int): The active breakpoint line number.
        """
        self.sequenceTreeView.set_active_breakpoint(active_breakpoint - self.sequenceTreeView.breakpoint_offset)

    def generate_code(self):
        import_model = self.importListView.model()
        variable_model = self.variableTableWidget.action_model()
        sequence_model = self.sequenceTreeView.model()
        tab = "    "
        code = ['""" Auto-Generated Code for sknrf Sequencer"""']
        code.append('')
        code.append('from sknrf.model.sequencer.base import AbstractSequencerRuntimeModel')
        code.append('')
        code.append('#  Module Import List')
        for index in range(import_model.rowCount()):
            py_code = import_model.item(index).data(ActionItemDataRole.CodeRole)
            for py_sub_code in py_code:
                code.append("# = ".join(py_sub_code)) if py_sub_code[0] else code.append("# " + py_sub_code[1])

        code.append('')
        code.append('')

        code.append('class SequencerRuntimeModel(AbstractSequencerRuntimeModel):')
        code.append(tab + '')
        code.append(tab + 'def measure(self):')
        code.append(tab + tab + '#  Variable Declaration Section')
        for index in range(variable_model.rowCount()):
            py_code = variable_model.item(index).data(ActionItemDataRole.CodeRole)
            for py_sub_code in py_code:
                code.append(tab + tab + "# " + " = ".join(py_sub_code)) if py_sub_code[0] else code.append(tab + tab + "# " + py_sub_code[1])
        code.append(tab + tab + '')

        code.append(tab + tab + '# Load Sequencer Namespace')
        code.append(tab + tab + 'self.connect_signals()')
        code.append(tab + tab + 'globals().update(self._locals)')
        code.append(tab + tab + 'try:')
        code.append(tab + tab + tab + '')

        code.append(tab + tab + tab + '#  Action Sequence Section')
        if not sequence_model.rowCount():
            code.append(tab + tab + tab + 'pass')
        else:
            self.sequenceTreeView.breakpoint_offset = len(code) + 1
            for index in range(sequence_model.rowCount()):
                py_code = sequence_model.item(index).data(ActionItemDataRole.CodeRole)
                for py_sub_code in py_code:
                    code.append(tab + tab + tab + " = ".join(py_sub_code)) if py_sub_code[0] else code.append(tab + tab + tab + py_sub_code[1])
            code.append(tab + tab + tab + '')

        code.append(tab + tab + 'finally:')
        code.append(tab + tab + tab + '#  Unload Sequencer Namespace')
        code.append(tab + tab + tab + 'for k in self._locals.keys():')
        code.append(tab + tab + tab + tab + 'globals().pop(k)')
        code.append(tab + tab + tab + 'self.disconnect_signals()')

        code = "\n".join(code)
        with open(os.sep.join((Settings().root, "sequencer_module.py")), "w") as file_id:
            file_id.write(code)
        dialog = CodeDialog(code, breakpoints=self.breakpoints(), parent=self)
        SequencerState.is_valid_code = True
        self.update(enabled=True)
        if dialog.exec():
            return

    def debugger_finished(self):
        self.variableTableWidget._model = self._base_variables
        self.sweep_preview_frame.set_model(self.variableTableWidget.model())
        if Settings().datagroup in self._model.datagroup_model():
            datagroup = self._model.datagroup_model()[Settings().datagroup]
            if datagroup.has_dataset(Settings().dataset):
                dataset = datagroup.dataset(Settings().dataset)
                self.signal_preview_frame.set_model(dataset)
        self.set_active_breakpoint(self.sequenceTreeView.breakpoint_offset - 1)

    def update_variables(self):
        self.update(variables=True)

    def update(self, frame=None, enabled=True, imports=False, variables=False, sequence=False, preview=False):
        """Updates the GUI.

        The entire menu will update by default.

        Keyword Args:
            frame (frame): Contains the state of all local variables during debug mode.
            enabled (bool): Update only the Enable state if True.
            imports (bool): Update only the Import List if True.
            variables (bool): Update only the Variable Table if True.
            sequence (bool): Update only the Sequence Tree if True.
        """
        super(SequencerFrame, self).update()
        all_ = not (enabled or imports or variables or sequence)

        if enabled or all_:
            self.setEnabled(True)

        if imports or all_:
            self.importListView.update()

        if variables or all_:
            self.variableTableWidget.update(frame)

        if sequence or all_:
            if frame:
                self.set_active_breakpoint(frame.f_lineno)
            self.sequenceTreeView.update()

        if preview or all_:
            self.sweep_preview_frame.set_model(self.variableTableWidget.model())
            if Settings().datagroup in self._model.datagroup_model():
                datagroup = self._model.datagroup_model()[Settings().datagroup]
                if datagroup.has_dataset(Settings().dataset):
                    dataset = datagroup.dataset(Settings().dataset)
                    self.signal_preview_frame.set_model(dataset)


class SequencerView(AbstractView, QMainWindow, Ui_sequencerMenu):
    """Sequencer Menu Window.

    ActionItems can be dragged from the left-hand ActionTreeView to one of three frames:

        1. Import List: Contains selected modules from the ActionTreeView.
        2. Variable Table: Contains selected instances of classes (objects) from the ActionTreeView.
        3. Sequence Tree: Contains selected functions/methods from the ActionTreeView.

    A Preview Tab Trame is provided for visualizing the state of Sweeps and Signals before and during debugging.

    The Debug mode allows the user to step through operations inside the Sequence Tree by clicking to set a breakpoint
    to the left of the row of interest. Upon reaching a breakpoint, three options are available to the user:

        1. Step: Execute current row and stop at the next row.
        2. Run: Run until the next breakpoint or the end of the sequence is reached.
        3. Stop: Stop execution and return to the initial state.

    Upon completion, the Sequencer Menu returns to the initial state.

    Keyword Args:
        model (SequencerModel): The model.
        parent (QWidget): Parent GUI container.
    """
    def __init__(self, device_model, datagroup_model, package_map, parent=None, model=None, base_class=AbstractModel):
        super(SequencerView, self).__init__(parent)
        self.setupUi(self)
        # Right Align Measurement Buttons of Toolbar
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionCode, empty)
        # Content Splitter
        self.splitter = QSplitter(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setSizePolicy(size_policy)
        self.sideViewTabWidget = SideViewTabWidget(parent=self.centralwidget)
        log_side_view = LogSideView(AbstractModel, logger, parent=self.sideViewTabWidget)

        # Initialize Models
        self.runtime_thread = RuntimeThread()
        self.runtime_model = None

        # Initialize Views
        self.sidebar_views = OrderedDict((("Sequencer", SequencerSideView(model=package_map, parent=self.sideViewTabWidget, base_class=base_class)),
                                          ("Main", MainSideView(model=AbstractModel, parent=self.sideViewTabWidget)),
                                          ("Log", log_side_view)))
        for tab_name, tab_widget in self.sidebar_views.items():
            self.sideViewTabWidget.addTab(tab_widget, tab_name)
        self.sequencerFrame = SequencerFrame(device_model, datagroup_model,
                                             parent=self.centralwidget, model=model)
        self.sequencerFrame.importListView.set_parent(self)
        self.sequencerFrame.variableTableWidget.set_parent(self)
        # self.sequencerFrame.selected_property_tab(None)
        self.sequencerFrame.sequenceTreeView.set_parent(self)
        self.runtime_view = None

        self.splitter.addWidget(self.sideViewTabWidget)
        self.splitter.addWidget(self.sequencerFrame)
        self.layout = self.centralwidget.layout()
        self.layout.addWidget(self.splitter)

        self.connect_signals()
        self.update()

    def connect_signals(self):
        self.sequencerFrame.connect_signals()

        self.actionNew.triggered.connect(self.clicked_new)
        self.actionLoad.triggered.connect(self.clicked_load)
        self.actionSave.triggered.connect(self.clicked_save)
        self.actionSave_As.triggered.connect(self.clicked_save_as)

        self.actionHelp.triggered.connect(self.clicked_doc)

        self.actionCode.triggered.connect(self.clicked_code)
        self.actionCompile.triggered.connect(self.clicked_compile)

        self.actionStep.triggered.connect(self.single)
        self.actionRun.triggered.connect(self.run)
        self.actionStop.triggered.connect(self.stop)

        self.sequencerFrame.importListView.model().rowsInserted.connect(self.sequence_changed)
        self.sequencerFrame.variableTableWidget.action_model().rowsInserted.connect(self.sequence_changed)
        self.sequencerFrame.sequenceTreeView.model().rowsInserted.connect(self.sequence_changed)
        self.sequencerFrame.importListView.model().dataChanged.connect(self.sequence_changed)
        self.sequencerFrame.variableTableWidget.action_model().dataChanged.connect(self.sequence_changed)
        self.sequencerFrame.sequenceTreeView.model().dataChanged.connect(self.sequence_changed)
        self.sequencerFrame.importListView.model().rowsRemoved.connect(self.sequence_changed)
        self.sequencerFrame.variableTableWidget.action_model().rowsRemoved.connect(self.sequence_changed)
        self.sequencerFrame.sequenceTreeView.model().rowsRemoved.connect(self.sequence_changed)

    def disconnect_signals(self):
        self.sequencerFrame.disconnect_signals()

        self.actionNew.triggered.disconnect()
        self.actionLoad.triggered.disconnect()
        self.actionSave.triggered.disconnect()
        self.actionSave_As.triggered.disconnect()

        self.actionHelp.triggered.disconnect()

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

    def sequence_changed(self, first, last):
        SequencerState.is_valid_code = False
        self.update(enabled=True)

    def setEnabled(self, enable):
        """Controls the enabled state of widgets when switching between setup and debug mode.

        Args:
            enable (bool): enable is True for setup mode and false for debug mode.
        """
        super(SequencerView, self).setEnabled(enable)
        is_running = enable and not RuntimeState.STOPPED
        is_runnable = enable & SequencerState.is_valid_code

        self.actionCompile.setEnabled(not is_running)
        self.actionNew.setEnabled(not is_running)
        self.actionLoad.setEnabled(not is_running)
        self.actionSave.setEnabled(not is_running)
        self.actionSave_As.setEnabled(not is_running)

        self.actionCode.setEnabled(not is_running)
        self.actionCompile.setEnabled(is_runnable and not is_running)
        self.actionStep.setEnabled(is_running)
        self.actionStep.setChecked(is_running)
        self.actionRun.setEnabled(is_runnable)
        self.actionRun.setChecked(is_running)
        self.actionStop.setEnabled(is_running)
        self.actionStop.setChecked(is_running)

        self.sideViewTabWidget.setEnabled(not is_running)

    def model(self):
        return self.sequencerFrame.model()

    def set_model(self, model):
        """Sets the model.

        Args:
            model (SequencerModel): The model.
        """
        self.sequencerFrame.set_model(model)
        self.update()

    def clicked_new(self):
        self.sequencerFrame.clear()

    def clicked_load(self):
        filenames = list()
        filename = "sequence.seq"
        filenames = QFileDialog.getOpenFileName(self,
                                                "Load Sequence",
                                                os.sep.join((Settings().data_root, "saved_sequences", filename)),
                                                "Sequence File (*.seq)")

        if len(filenames[0]):
            filename = filenames[0]
            old_model = self.model()
            self.disconnect_signals()
            if sys.platform == "win32": pythoncom.CoInitialize()
            try:
                model, module_row, variable_row, action_row = pickle.load(open(filename, "rb"))
            except pickle.UnpicklingError:
                QMessageBox.critical(self, 'Unable to Load Saved Sequence',
                                           'Saved state contains modules, variables or actions that are no longer valid')
                self.set_model(old_model)
            else:
                self.set_model(model)
                self.sequencerFrame.importListView.setCurrentIndex(self.sequencerFrame.importListView.model().index(module_row, 0))
                if variable_row >= 0:
                    item = self.sequencerFrame.variableTableWidget.topLevelItems()[variable_row]
                    self.sequencerFrame.variableTableWidget.setCurrentItem(item)
                self.sequencerFrame.sequenceTreeView.setCurrentIndex(self.sequencerFrame.sequenceTreeView.model().index(action_row, 0))
            self.connect_signals()

    def clicked_save(self):
        filenames = list()
        filename = "sequence.seq"
        filenames = QFileDialog.getSaveFileName(self,
                                                "Save Sequence",
                                                os.sep.join((Settings().data_root, "saved_sequences", filename)),
                                                "Sequence File (*.seq)")

        if len(filenames[0]):
            filename = filenames[0]
            try:
                module_row = self.sequencerFrame.importListView.currentIndex().row()
                selected_item = self.sequencerFrame.variableTableWidget.currentItem()
                variable_items = self.sequencerFrame.variableTableWidget.topLevelItems()
                variable_row = variable_items.index(selected_item) if selected_item in variable_items else -1
                action_row = self.sequencerFrame.sequenceTreeView.currentIndex().row()
                pickle.dump((self.model(), module_row, variable_row, action_row), open(filename, "wb"))
            except pickle.PicklingError:
                QMessageBox.critical(self, 'Unable to Save Sequence',
                                           'Saved state contains modules, variables or actions that cannot be pickled')
                os.remove(filename)

    def clicked_save_as(self):
        pass

    def clicked_store(self):
        pass

    def clicked_code(self):
        self.sequencerFrame.generate_code()
        self.update()

    def clicked_compile(self):
        pass

    @QtCore.Slot(bool)
    def run(self, checked=False):
        sequencer_module = importlib.import_module("sknrf.sequencer_module")
        sequencer_module = importlib.reload(sequencer_module)
        variables = self.sequencerFrame.variableTableWidget.model()
        self.sequencerFrame._base_variables = self.sequencerFrame.variableTableWidget.model()

        self.runtime_thread = RuntimeThread()
        self.runtime_view = LargeSignalRuntimeView()
        self.runtime_model = sequencer_module.SequencerRuntimeModel(variables)
        for k,v in variables.items():
            if isinstance(v, AbstractModel):
                variables[k].moveToThread(self.runtime_thread)

        self.runtime_thread.connect_signals(self.runtime_model, self.runtime_view)
        self.runtime_thread.started_.connect(self.runtime_model.measure)  # Pycharm Debugger does not work with Qthread.started
        self.runtime_thread.finished.connect(self.update)
        self.runtime_model.stimulus_ports = list(range(0, Settings().num_ports + 1))
        self.runtime_model.ss_stimulus_ports = list(range(0, Settings().num_ports + 1))
        # self.debugger_thread.user_response = None
        # for line_number in self.sequencerFrame.breakpoints():
        #     self.debugger_thread.set_break(os.sep.join((Settings().root, "sequencer_module.py")), line_number)
        self.runtime_thread.start()

    @QtCore.Slot(bool)
    def single(self, checked=False):
        self.update()

    @QtCore.Slot(bool)
    def pause(self, checked=False):
        self.update()

    @QtCore.Slot(bool)
    def stop(self, checked=False):
        self.update()

    def closeEvent(self, event):
        Settings().datagroup = "Single"
        Settings().dataset = "Single"
        event.accept()

    def update(self, sideview=False, frame=None, enabled=False, imports=False, variables=False, sequence=False, preview=False):
        """Updates the GUI.

        The entire menu will update by default.

        Keyword Args:
            frame (frame): Contains the state of all local variables during debug mode.
            enabled (bool): Update only the Enable state if True.
            imports (bool): Update only the Import List if True.
            variables (bool): Update only the Variable Table if True.
            sequence (bool): Update only the Sequence Tree if True.
        """
        super(SequencerView, self).update()
        all_ = not (sideview or frame or enabled or imports or variables or sequence or preview)

        if enabled or all_:
            self.setEnabled(True)
        if sideview or all_:
            self.sideViewTabWidget.update()
        self.sequencerFrame.update(frame=frame, enabled=enabled,
                                   imports=imports, variables=variables, sequence=sequence, preview=preview)

    def debugger_finished(self):
        self.sequencerFrame.debugger_finished()
        self.update()

