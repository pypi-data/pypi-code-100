"""
    ============================
    Base Calibration Wizard View
    ============================

    This module defines the default behaviour of the Calibration Wizard.
    See Also
    ----------
    sknrf.model.base.AbstractModel
"""

import abc
import os
import pickle
import re
from functools import reduce

import numpy as np
import skrf
from PySide2 import QtCore
from PySide2.QtCore import QSize, QSignalMapper
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QDialog, QFileDialog, QFrame, QWizard, QWizardPage, QLabel, QCheckBox, QPushButton, QComboBox, QSpacerItem
from PySide2.QtWidgets import QGridLayout, QVBoxLayout, QSizePolicy
from skrf.network import cascade

from sknrf.settings import Settings, InstrumentFlag
from sknrf.model.calibration.base import AbstractCalibrationModel
from sknrf.model.calibration.base import label_instrument_map, instrument_enable_map, calkit_connector_map
from sknrf.model.runtime import RuntimeThread
from sknrf.utilities.patterns import CaseInsensitiveDict
from sknrf.view.base import AbstractView
from sknrf.view.desktop.base import BusyFrame
from sknrf.view.desktop.calibration.QCalibration import Ui_calibrationWizard
from sknrf.view.desktop.device.menu import DeviceMenuView
from sknrf.view.desktop.runtime.ls import LargeSignalRuntimeView
from sknrf.view.desktop.runtime.ss import SmallSignalRuntimeView

component_image_map = CaseInsensitiveDict({
    "Short": ":/PNG/black/64/short2.png",
    "Open": ":/PNG/black/64/open2.png",
    "Load": ":/PNG/black/64/load2.png",
    "Delay": ":/PNG/black/64/delay.png",
    "Delay1": ":/PNG/black/64/delay.png",
    "Delay2": ":/PNG/black/64/delay.png",
    "Reflect": ":/PNG/black/64/reflect.png",
    "__HalfKnownReflection": ":/PNG/black/64/reflection.png",
    "__Reflection": ":/PNG/black/64/reflection.png",
    "Thru": ":/PNG/black/64/thru2.png",
    "Thru with B Wave Attenuator Connected SS": ":/PNG/black/64/thru2.png",
    "Thru with B Wave Attenuator NOT Connected SS": ":/PNG/black/64/thru2.png",
    "Line": ":/PNG/black/64/line2.png",
    "__Transmission": ":/PNG/black/64/transmission.png",
    "__Unknown": ":/PNG/black/64/unknown2.png",
    "Adapter": ":/PNG/black/64/adaptor.png",
    "Port": ":/PNG/black/64/port_right.png",
    "Port0": ":/PNG/black/64/port_right.png",
    "Port1": ":/PNG/black/64/port_right.png",
    "Port2": ":/PNG/black/64/port_right.png",
    "Port0 ": ":/PNG/black/64/port_left.png",
    "Port1 ": ":/PNG/black/64/port_left.png",
    "Port2 ": ":/PNG/black/64/port_left.png",
    "LFSourceRef": ":/PNG/black/64/lfsource_ref.png",
    "LFReceiverRef": ":/PNG/black/64/lfreceiver_ref.png",
    "RFSourceRef": ":/PNG/black/64/rfsource_ref.png",
    "RFReceiverRef": ":/PNG/black/64/rfreceiver_ref.png",
})

custom_component_list = ("Short", "Open", "Load", "Delay", "Reflect",
                         "Thru", "Line", "Adapter",
                         "__HalfKnownReflection", "__Reflection",
                         "__Transmission", "__Unknown")


class ComponentButton(QPushButton):

    def __init__(self, *args, parent=None):
        super(ComponentButton, self).__init__(*args, parent=parent)
        self.setMinimumSize(QSize(10, 10))
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setSizePolicy(size_policy)
        self.setFlat(self.text() not in custom_component_list)
        self.setText("")

    def resizeEvent(self, event):
        super(ComponentButton, self).resizeEvent(event)
        self.setIconSize(QSize(event.size().width()-10, event.size().height()-10))


class AbstractPortPage(QWizardPage):

    def __init__(self, _parent):
        super(AbstractPortPage, self).__init__(parent=_parent)
        self._parent = _parent
        self.setTitle("Calibration Name")
        self.setSubTitle("Port Connections")
        self.portCheckBoxSignalMapper = QSignalMapper()
        self.portComboBoxSignalMapper = QSignalMapper()
        self.adapterPushButtonSignalMapper = QSignalMapper()
        self.calkitComboBoxSignalMapper = QSignalMapper()

        self.vbl = QVBoxLayout(self)
        self.portsFrame = QFrame(parent=self)
        self.portsFrame.setFrameShape(QFrame.WinPanel)
        self.portsFrame.setFrameShadow(QFrame.Raised)
        self.gbl = QGridLayout(self.portsFrame)
        self.portConnectorLabel = QLabel("Port connector", parent=self.portsFrame)
        self.portAdapterLabel = QLabel("Adapter", parent=self.portsFrame)
        self.calkitConnectorLabel = QLabel("Calkit connector", parent=self.portsFrame)
        self.gbl.addWidget(self.portConnectorLabel, 0, 1, 1, 1)
        self.gbl.addWidget(self.portAdapterLabel, 0, 2, 1, 1)
        self.gbl.addWidget(self.calkitConnectorLabel, 0, 3, 1, 1)

        self.portCheckBoxList = list()
        self.portComboBoxList = list()
        self.adapterPushButtonList = list()
        self.calkitComboBoxList = list()
        connector_names = list(calkit_connector_map.keys())
        for port_index in range(Settings().num_ports):
            port_num = port_index + 1
            self.portCheckBoxList.append(QCheckBox("Port " + str(port_num), parent=self.portsFrame))
            self.portComboBoxList.append(QComboBox(parent=self.portsFrame))
            self.portComboBoxList[port_index].addItems(connector_names)
            self.adapterPushButtonList.append(QPushButton("...", parent=self.portsFrame))
            self.calkitComboBoxList.append(QComboBox(parent=self.portsFrame))
            self.calkitComboBoxList[port_index].addItems(connector_names)
            self.gbl.addWidget(self.portCheckBoxList[port_index], port_index+1, 0, 1, 1)
            self.gbl.addWidget(self.portComboBoxList[port_index], port_index+1, 1, 1, 1)
            self.gbl.addWidget(self.adapterPushButtonList[port_index], port_index+1, 2, 1, 1)
            self.gbl.addWidget(self.calkitComboBoxList[port_index], port_index+1, 3, 1, 1)
        self.vbl.addWidget(self.portsFrame)
        self.setLayout(self.vbl)
        self.connect_signals()

    def connect_signals(self):
        pass
        # for port_index in range(Settings().num_ports):
        #     self.portCheckBoxList[port_index].stateChanged.connect(self.portCheckBoxSignalMapper.map)
        #     self.portCheckBoxSignalMapper.setMapping(self.portCheckBoxList[port_index], port_index)
        #     self.portComboBoxList[port_index].currentIndexChanged[str].connect(self.portComboBoxSignalMapper.map)
        #     self.portComboBoxSignalMapper.setMapping(self.portComboBoxList[port_index], port_index)
        #     self.adapterPushButtonList[port_index].clicked.connect(self.adapterPushButtonSignalMapper.map)
        #     self.adapterPushButtonSignalMapper.setMapping(self.adapterPushButtonList[port_index], port_index)
        #     self.calkitComboBoxList[port_index].currentIndexChanged[str].connect(self.calkitComboBoxSignalMapper.map)
        #     self.calkitComboBoxSignalMapper.setMapping(self.calkitComboBoxList[port_index], port_index)
        # self.portCheckBoxSignalMapper.mapped.connect(self.set_port_indices)
        # self.portComboBoxSignalMapper.mapped.connect(self.set_port_connector)
        # self.adapterPushButtonSignalMapper.mapped.connect(self.load_adapter)
        # self.calkitComboBoxSignalMapper.mapped.connect(self.set_calkit_connector)

    def disconnect_signals(self):
        pass
        # self.portCheckBoxSignalMapper.mapped.disconnect(self.set_port_indices)
        # self.portComboBoxSignalMapper.mapped.disconnect(self.set_port_connector)
        # self.adapterPushButtonSignalMapper.mapped.disconnect(self.load_adapter)
        # self.calkitComboBoxSignalMapper.mapped.disconnect(self.set_calkit_connector)
        # for port_index in range(Settings().num_ports):
        #     self.portCheckBoxList[port_index].stateChanged.disconnect(self.portCheckBoxSignalMapper.map)
        #     self.portCheckBoxSignalMapper.setMapping(self.portCheckBoxList[port_index], port_index)
        #     self.portComboBoxList[port_index].currentIndexChanged[str].disconnect(self.portComboBoxSignalMapper.map)
        #     self.portComboBoxSignalMapper.setMapping(self.portComboBoxList[port_index], port_index)
        #     self.adapterPushButtonList[port_index].clicked.disconnect(self.adapterPushButtonSignalMapper.map)
        #     self.adapterPushButtonSignalMapper.setMapping(self.adapterPushButtonList[port_index], port_index)
        #     self.calkitComboBoxList[port_index].currentIndexChanged[str].disconnect(self.calkitComboBoxSignalMapper.map)
        #     self.calkitComboBoxSignalMapper.setMapping(self.calkitComboBoxList[port_index], port_index)

    def wizard(self):
        return self._parent

    def set_port_indices(self, port_index):
        enable = self.portCheckBoxList[port_index].isChecked()
        port_indices = self.wizard().port_indices()
        if enable and port_index not in port_indices:
            port_indices.append(port_index)
        if not enable and port_index in port_indices:
            port_indices.remove(port_index)
        self.wizard().set_port_indices(port_indices)
        self.update(state=True)

    @QtCore.Slot(str)
    def set_port_connector(self, port_index):
        connector = self.portComboBoxList[port_index].currentText()
        self.wizard().set_port_connector(port_index, connector)
        self.update(state=True)

    def load_adapter(self, port_index):
        filenames = QFileDialog.getOpenFileName(self,
                                                "Load Adapter S-Parameter File",
                                                os.sep.join((Settings().data_root, "caldata")),
                                                "S-Parameter File (*.s2p)")
        if len(filenames[0]):
            filename = filenames[0]
            self.wizard().set_adapter_filename(port_index, filename)
        self.update(state=True)

    @QtCore.Slot(str)
    def set_calkit_connector(self, port_index):
        connector = self.calkitComboBoxList[port_index].currentText()
        self.wizard().set_calkit_connector(port_index, connector)
        self.update(state=True)

    def isComplete(self):
        """ Defines the conditions that must be satisfied befor proceeding to the the next page.
        """
        return len(self.wizard().port_indices()) > 0

    def update(self, state=False):
        super(AbstractPortPage, self).update()
        all_ = not state

        if self.wizard() and state or all_ :
            load_button = self.wizard().button(QWizard.CustomButton1)
            load_button.setVisible(False)

            for port_index in range(Settings().num_ports):
                enable = self.portCheckBoxList[port_index].isChecked()
                self.portComboBoxList[port_index].setEnabled(enable)
                self.calkitComboBoxList[port_index].setEnabled(enable)
                port_connector = self.wizard().port_connector(port_index)
                calkit_connector = self.wizard().calkit_connector(port_index)
                self.adapterPushButtonList[port_index].setEnabled(enable and port_connector != calkit_connector)
                self.adapterPushButtonList[port_index].setText(port_connector + "/" + calkit_connector)
            self.completeChanged.emit()


class AbstractInstrumentPage(QWizardPage):
    def __init__(self, _parent):
        super(AbstractInstrumentPage, self).__init__(parent=_parent)
        self._parent = _parent
        self.setTitle("Instrument Selection")
        self.setSubTitle("Select the instruments where the calibration will be applied")
        self.instrumentCheckBoxSignalMapper = QSignalMapper()

        self.vbl = QVBoxLayout(self)
        self.instrumentsFrame = QFrame(parent=self)
        self.instrumentsFrame.setFrameShape(QFrame.WinPanel)
        self.instrumentsFrame.setFrameShadow(QFrame.Raised)
        self.instrumentsGBL = QGridLayout(self.instrumentsFrame)
        self.instrumentsLabel = QLabel("Port Instruments:", parent=self.instrumentsFrame)
        self.instrumentsGBL.addWidget(self.instrumentsLabel, 0, 0, 1, 1)
        self.instrumentsCheckBoxList = list()
        self.vbl.addWidget(self.instrumentsFrame)

        self.connect_signals()

    def connect_signals(self):
        pass
        # for index in range(len(self.instrumentsCheckBoxList)):
        #     self.instrumentsCheckBoxList[index].stateChanged.connect(self.instrumentCheckBoxSignalMapper.map)
        #     self.instrumentCheckBoxSignalMapper.setMapping(self.instrumentsCheckBoxList[index], index)
        # self.instrumentCheckBoxSignalMapper.mapped.connect(self.set_instrument)

    def disconnect_signals(self):
        pass
        # for index in range(len(self.instrumentsCheckBoxList)):
        #     self.instrumentsCheckBoxList[index].stateChanged.disconnect()
        #     self.instrumentCheckBoxSignalMapper.setMapping(self.instrumentsCheckBoxList[index], index)
        # self.instrumentCheckBoxSignalMapper.mapped.disconnect()

    def wizard(self):
        return self._parent

    def add_instrument(self, instrument_flags, checked_map=instrument_enable_map):
        self.disconnect_signals()
        for index, (k, v) in enumerate(label_instrument_map.items()):
            if v & instrument_flags:
                check_box = QCheckBox(k, parent=self)
                check_box.setChecked(checked_map[v])
                self.instrumentsCheckBoxList.append(check_box)
                self.instrumentsGBL.addWidget(self.instrumentsCheckBoxList[-1], self.instrumentsGBL.rowCount(), 0, 1, 1)
        self.set_instrument(0)
        self.connect_signals()

    def set_instrument(self, index):
        instrument_flags = 0
        for checkbox in self.instrumentsCheckBoxList:
            if checkbox.isChecked():
                instrument_flags |= label_instrument_map[checkbox.text()]
        self.wizard().set_instrument(instrument_flags)
        self.update(state=True)

    def isComplete(self):
        """ Defines the conditions that must be satisfied before proceeding to the the next page.
        """
        for instrumentsCheckBox in self.instrumentsCheckBoxList:
            if instrumentsCheckBox.isChecked():
                return True
        return False

    def update(self, state=False):
        super(AbstractInstrumentPage, self).update()
        all_ = not state

        if self.wizard() and state or all_:
            load_button = self.wizard().button(QWizard.CustomButton1)
            load_button.setVisible(False)
            self.completeChanged.emit()


class AbstractRequirementsPage(QWizardPage):
    """The default Calibration Wizard Introduction Page.

        Each Calibration Introduction page contains a list of custom:

            * Requirements: Mandatory conditions that must be satisfied before performing this calibration.
            * Recommendations: Optional conditions that should be satisfied to maximize calibration accuracy.

        Each requirement and recommendation is represented by a checkbox. The recommendations can be manually checked by
        the user. The Calibration Wizard can only proceed when all requirements and recommendations are satisfied.

        See Also
        ----------
        AbstractCalibrationWizard, AbstractContentPage, AbstractConclusionPage
    """

    def __init__(self, _parent):
        super(AbstractRequirementsPage, self).__init__(parent=_parent)
        self._parent = _parent
        self.setTitle("Calibration Name")
        self.setSubTitle("Calibration Description")
        self.recommendationsCheckBoxSignalMapper = QSignalMapper()

        self.vbl = QVBoxLayout(self)
        self.requirementsFrame = QFrame(parent=self)
        self.requirementsFrame.setFrameShape(QFrame.WinPanel)
        self.requirementsFrame.setFrameShadow(QFrame.Raised)
        self.requirementsGBL = QGridLayout(self.requirementsFrame)
        self.requirementsLabel = QLabel("Calibration Requirements:", parent=self.requirementsFrame)
        self.requirementsGBL.addWidget(self.requirementsLabel, 0, 0, 1, 1)
        self.requirementsCheckBoxList = list()
        self.vbl.addWidget(self.requirementsFrame)

        self.recommendationsFrame = QFrame(parent=self)
        self.recommendationsFrame.setFrameShape(QFrame.WinPanel)
        self.recommendationsFrame.setFrameShadow(QFrame.Raised)
        self.recommendationsGBL = QGridLayout(self.recommendationsFrame)
        self.recommendationsLabel = QLabel("Calibration Recommendations:", parent=self.recommendationsFrame)
        self.recommendationsGBL.addWidget(self.recommendationsLabel, 0, 0, 1, 1)
        self.recommendationsCheckBoxList = list()
        self.vbl.addWidget(self.recommendationsFrame)

    def wizard(self):
        return self._parent

    def connect_signals(self):
        pass
        # for index in range(len(self.recommendationsCheckBoxList)):
        #     self.recommendationsCheckBoxList[index].stateChanged.connect(self.recommendationsCheckBoxSignalMapper.map)
        #     self.recommendationsCheckBoxSignalMapper.setMapping(self.recommendationsCheckBoxList[index], index)
        # self.recommendationsCheckBoxSignalMapper.mapped.connect(self.set_recommendations)

    def disconnect_signals(self):
        pass
        # for index in range(len(self.recommendationsCheckBoxList)):
        #     self.recommendationsCheckBoxList[index].stateChanged.disconnect()
        #     self.recommendationsCheckBoxSignalMapper.setMapping(self.recommendationsCheckBoxList[index], index)
        # self.recommendationsCheckBoxSignalMapper.mapped.connect()

    def add_requirement(self, requirement_str):
        """ Adds a READ ONLY Requirement check-box to the page.
        """
        self.requirementsCheckBoxList.append(QCheckBox(requirement_str, parent=self))
        self.requirementsGBL.addWidget(self.requirementsCheckBoxList[-1], self.requirementsGBL.rowCount(), 0, 1, 1)

    def add_recommendation(self, recommendation_str):
        """ Adds a recommendation check-box to the page.
            """
        self.recommendationsCheckBoxList.append(QCheckBox(recommendation_str, parent=self))
        self.recommendationsGBL.addWidget(self.recommendationsCheckBoxList[-1], self.recommendationsGBL.rowCount(), 0, 1, 1)

    @abc.abstractmethod
    def check_requirements(self):
        """ Checks the status of each requirement and automatically defines the state of each requirement checkbox.
        """
        for requirementsCheckBox in self.requirementsCheckBoxList:
            requirementsCheckBox.setEnabled(False)

    @abc.abstractmethod
    def check_recommendations(self):
        """ Checks the status of each recommendation and defines the default state of each recommendation checkbox.
        """
        for recommendationsCheckBox in self.recommendationsCheckBoxList:
            recommendationsCheckBox.setEnabled(True)

    def set_recommendations(self, index=-1):
        self.update(state=True, recommendations=False)

    def isComplete(self, index=-1):
        """ Defines the conditions that must be satisfied before proceeding to the the next page.
        """
        for requirementsCheckBox in self.requirementsCheckBoxList:
            if not requirementsCheckBox.isChecked():
                return False
        for recommendationsCheckBox in self.recommendationsCheckBoxList:
            if not recommendationsCheckBox.isChecked():
                return False
        return True

    def update(self, state=False, recommendations=False):
        super(AbstractRequirementsPage, self).update()
        all_ = not (state or recommendations)

        if self.wizard() and state or all_:
            if not self.wizard().settings_are_current:
                self.wizard().initialize_content_pages()
            load_button = self.wizard().button(QWizard.CustomButton1)
            load_button.setText("Load")
            load_button.setVisible(True)
            self.check_requirements()
            if recommendations or all_:
                self.check_recommendations()
            self.completeChanged.emit()


class AbstractContentPage(QWizardPage):
    """The default Calibration Wizard Content Page.

        Each Calibration Content page defines an OrderedDict of components that should be connected by the user. The
        ``Measure`` button must be pressed in order to proceed to the next page.

        Parameters
        ----------
        name : str
            Name of the calibration step.
        component_names : list
            A list of component names.
        optional : bool
            Defines whether the calibration step is optional.

        See Also
        ----------
        AbstractCalibrationWizard, AbstractIntroductionPage, AbstractConclusionPage
    """

    def __init__(self, _parent, name="", component_names=(), optional=False):
        super(AbstractContentPage, self).__init__(parent=_parent)
        self._parent = _parent
        self.name = name
        self.step_num = 0
        self.optional = optional
        self.component_names = list(component_names)
        self.ntwks = [None] * len(component_names)
        self.pushButtonSignalMapper = QSignalMapper()

        self.gbl = QGridLayout(self)
        x_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gbl.addItem(x_spacer, 0, 0, 1, 1)
        self.componentPushButtons, index = [], 1

        for component_name in self.component_names:
            component_image = component_image_map[component_name] if component_name in component_image_map \
                else component_image_map["__Unknown"]
            icon = QIcon(QPixmap(component_image))
            self.componentPushButtons.append(ComponentButton(icon, component_name, parent=self))
            self.gbl.addWidget(self.componentPushButtons[-1], 0, index, 1, 1)
            index += 1
        x_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gbl.addItem(x_spacer, 0, index, 1, 1)
        self.setLayout(self.gbl)

        self.connect_signals()

    def connect_signals(self):
        pass
        # index = 0
        # for componentPushButton in self.componentPushButtons:
        #     componentPushButton.clicked.connect(self.pushButtonSignalMapper.map)
        #     self.pushButtonSignalMapper.setMapping(componentPushButton, index)
        #     index += 1
        # self.pushButtonSignalMapper.mapped.connect(self.load_ideal)

    def disconnect_signals(self):
        pass
        # index = 0
        # for componentPushButton in self.componentPushButtons:
        #     componentPushButton.clicked.disconnect(self.pushButtonSignalMapper.map)
        #     self.pushButtonSignalMapper.setMapping(componentPushButton, index)
        #     index += 1
        # self.pushButtonSignalMapper.mapped.disconnect(self.load_ideal)

    def wizard(self):
        return self._parent

    def name_info(self, component_index=-1, filename=""):
        page_name, port_nums = AbstractCalibrationModel.name_info(self.name)
        old_name = re.sub(r"_\d", "", self.component_names[component_index])
        new_name = re.sub(r"_\d", "", os.path.splitext(os.path.basename(filename))[0]) if len(filename) else ""
        return page_name, port_nums, old_name, new_name

    def load_ideal(self, component_index):
        if not self.componentPushButtons[component_index].isFlat():
            self.wizard().load_ideal(component_index)

    def set_ideal(self, component_index, filename):
        _, _, _, new_name = self.name_info(component_index, filename)
        component_image = component_image_map[new_name] if new_name in component_image_map else component_image_map["__Unknown"]
        icon = QIcon(QPixmap(component_image))
        self.component_names[component_index] = new_name
        self.componentPushButtons[component_index].setIcon(icon)
        self.update(state=True)

    def update(self, state=False):
        super(AbstractContentPage, self).update()
        all_ = not state

        if self.wizard() and state or all_:
            optional_str = " [Optional]" if self.optional else ""
            self.setTitle("Step: %d of %d%s" % (self.step_num, self.wizard().num_steps, optional_str))
            subtitle = "to ".join(["%s "] * len(self.component_names))
            self.setSubTitle("Connect " + subtitle % tuple(self.component_names))
            measure_button = self.wizard().button(QWizard.CustomButton1)
            measure_button.setText("Measure")
            measure_button.setVisible(True)
            self.completeChanged.emit()


class AbstractConclusionPage(QWizardPage):
    """The default Calibration Wizard Conclusion Page.

        Each Calibration Conclusion page calculates the error-correction when the page is updated and applies it when
        the ``finish`` button is clicked.

        See Also
        ----------
        AbstractCalibrationWizard, AbstractIntroductionPage, AbstractContentPage
    """

    def __init__(self, _parent=None):
        super(AbstractConclusionPage, self).__init__(parent=_parent)
        self._parent = _parent
        self.setTitle("Finished")
        self.setSubTitle("Calibration Completed")
        self._calibration_passed = False

    def wizard(self):
        return self._parent

    @property
    def calibration_passed(self):
        return self._calibration_passed

    @calibration_passed.setter
    def calibration_passed(self, value):
        if self._calibration_passed != value:
            self._calibration_passed = value
            self.update(state=True, cal=False)

    def isComplete(self):
        """ Defines the conditions that must be satisfied befor proceeding to the the next page.
        """
        return self._calibration_passed

    def update(self, state=False, cal=False):
        super(AbstractConclusionPage, self).update()
        all_ = not (state or cal)

        if self.wizard() and state or all_:
            save_button = self.wizard().button(QWizard.CustomButton1)
            save_button.setText("Save")
            save_button.setVisible(True)
            save_button.setEnabled(self.calibration_passed)
            self.completeChanged.emit()

        if cal or all_:
            try:
                self.wizard().calculate()
            except ValueError as e:
                self.setTitle("Calibration Failed")
                self.setSubTitle(str(e))
                self.calibration_passed = False
            else:
                self.setTitle("Calibration Passed")
                self.calibration_passed = True


class AbstractCalibrationWizard(QWizard, Ui_calibrationWizard, AbstractView):
    """The default Calibration Wizard.

        The Calibration Wizard defines a sequential calibration wizard consisting of the following pages:

            * AbstractIntroductionPage.
            * AbstractContentPage.
            * AbstractConclusionPage.

        See Also
        ----------
        AbstractIntroductionPage, AbstractContentPage, AbstractConclusionPage
    """
    calkit_loaded = QtCore.Signal(object, object)
    calkit_removed = QtCore.Signal(object)
    single_measurement = QtCore.Signal()
    calkit_menu_closed = QtCore.Signal()
    loaded_calibration = QtCore.Signal()

    def __init__(self, parent=None, calkit_package=None, calkit_icon=QIcon()):
        super(AbstractCalibrationWizard, self).__init__(parent=parent)
        self.setupUi(self)
        self.setButtonText(QWizard.CustomButton1, "Measure")

        self.menuButton = QPushButton(calkit_icon, "", parent=None)
        self.menuButton.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.menuButton.setIconSize(QSize(64, 64))
        self.calkit_package = calkit_package
        self._calkit_model = None
        self.calkit_menu = None

        self.num_steps = 0
        self.num_extra_steps = 0
        self._calibration_passed = False
        self.settings_are_current = False
        self._runtime_thread = RuntimeThread()
        self._runtime_view = None
        self._runtime_model = None
        self.connect_signals()

    def connect_signals(self):
        pass
        # super(AbstractCalibrationWizard, self).connect_signals()
        # self.menuButton.clicked.connect(self.clicked_menu_button)
        #
        # self.helpRequested.connect(self.clicked_doc)
        # self.customButtonClicked.connect(self.custom_clicked)
        # self.currentIdChanged.connect(self.page_changed)

    def disconnect_signals(self):
        pass
        # super(AbstractCalibrationWizard, self).disconnect_signals()
        # self.menuButton.clicked.disconnect()
        #
        # self.helpRequested.disconnect()
        # self.customButtonClicked.disconnect()
        # self.currentIdChanged.disconnect()

    def show(self):
        if self.wizardStyle() & (QWizard.ModernStyle | QWizard.ClassicStyle):
            self.restart()
            banner = self.children()[0].children()[-1]
            banner_layout = banner.layout()
            last_widget = banner_layout.itemAt(banner_layout.count()-1).widget()
            if isinstance(last_widget, QLabel):
                self.menuButton.setParent(banner)
                banner_layout.addWidget(self.menuButton, 0, banner_layout.columnCount(), banner_layout.rowCount(), 1)
        super(AbstractCalibrationWizard, self).show()

    def set_model(self, model, calkit_model):
        self.disconnect_signals()
        self._model = model
        self._calkit_model = calkit_model
        self.connect_signals()

    def insert_content_pages(self, new_pages, page_id=-1):
        """ Insert a content page into the wizard before page_id.
        """
        for page in new_pages:
            _, port_nums, _, _ = page.name_info(0)
            port_indices = np.array(list(filter(None, port_nums.split("_")))).astype(np.int) - 1
            adapter_indices = [x for x in range(len(page.component_names)) if page.component_names[x] == "Adapter"]
            for index in range(len(adapter_indices)):
                adapter_filename = self.adapter_filename(port_indices[index])
                if adapter_filename:
                    self.set_ideal(adapter_indices[index], adapter_filename, page)

        pages = list()
        for id in reversed(self.pageIds()):
            page = self.page(id)
            if id == page_id:
                break
            elif isinstance(page, AbstractConclusionPage):
                pages.append(page)
                self.removePage(id)
            elif isinstance(page, AbstractContentPage):
                self.num_steps -= 1
                if page.optional:
                    self.num_extra_steps -= 1
                pages.append(page)
                self.removePage(id)
            elif page_id < 0:
                break
            else:
                raise ValueError("Unable to insert content page before Connection or Introduction Page")
        pages += reversed(new_pages)
        for page in reversed(pages):
            if isinstance(page, AbstractContentPage):
                self.num_steps += 1
                if page.optional:
                    self.num_extra_steps += 1
                page.step_num = self.num_steps
            self.addPage(page)
        self.currentPage().setFinalPage(False)
        self.settings_are_current = True

    @abc.abstractmethod
    def insert_optional_content_page(self):
        pass

    @abc.abstractmethod
    def initialize_content_pages(self):
        for page_id in self.pageIds():
            if isinstance(self.page(page_id), AbstractContentPage):
                self.removePage(page_id)

    def port_indices(self, ):
        return [index - 1 for index in self._model.port_indices]

    def set_port_indices(self, port_indices):
        self._model.port_indices = [index + 1 for index in port_indices]
        self.settings_are_current = False

    def port_connector(self, port_index):
        return self._model.port_connectors[port_index]

    def set_port_connector(self, port_index, connector):
        self._model.port_connectors[port_index] = connector
        self.settings_are_current = False

    def adapter_filename(self, port_index):
        return self._model.adapter_filenames[port_index]

    def set_adapter_filename(self, port_index, filename):
        self._model.adapter_filenames[port_index] = filename
        self.settings_are_current = False

    def calkit_connector(self, port_index):
        return self._model.calkit_connectors[port_index]

    def set_calkit_connector(self, port_index, connector):
        self._model.calkit_connectors[port_index] = connector
        self.settings_are_current = False

    def set_instrument(self, instrument_flags):
        self._model.instrument_flags = instrument_flags
        self.settings_are_current = False

    def clicked_menu_button(self, checked=False):
        self.menu = DeviceMenuView(self.calkit_package, self._calkit_model,
                                   model_icon=self.menuButton.icon(), parent=self)
        self.menu.actionSingle.setEnabled(False)
        self.menu.sidebar_views["Device"].driverComboBox.setEnabled(False)
        self.menu.sidebar_views["Device"].testButton.setEnabled(False)
        self.menu.sidebar_views["Device"].loadDriverButton.setEnabled(False)

        self.menu.device_loaded.connect(self.__load_driver)
        self.menu.device_removed.connect(self.__remove_driver)
        self.menu.single_measurement.connect(self.__single_measurement)
        self.menu.show()

    def page_changed(self, id):
        """ Update the contents of the new page.
        """
        current_page = self.currentPage()
        if current_page:
            self.currentPage().update()

    def custom_clicked(self, which):
        """ Update the contents of the new page.
        """
        if which == QWizard.CustomButton1:
            current_page = self.currentPage()
            if isinstance(current_page, AbstractRequirementsPage):
                self.load()
            elif isinstance(current_page, AbstractContentPage):
                self.measure()
            elif isinstance(current_page, AbstractConclusionPage):
                self.save()

    def __load_driver(self, calkit_model):
        old_model = self._calkit_model
        self.calkit_loaded.emit(old_model, calkit_model)

    def __remove_driver(self):
        old_model = self._calkit_model
        self._calkit_model = None
        self.calkit_removed.emit(old_model)

    def __single_measurement(self):
        self.single_measurement.emit()

    def __menu_closed(self, calkit_model):
        self.set_model(self._model, calkit_model)
        self.calkit_menu_closed.emit()

    def run(self):
        """ Opens the calibration wizard.
        """
        self.show()

    def load(self):
        filenames = QFileDialog.getOpenFileName(self,
                                                "Load Calibration",
                                                os.sep.join((Settings().data_root, "saved_calibrations")),
                                                "Calibration File (*.cal)")

        if len(filenames[0]):
            filename = filenames[0]
            with BusyFrame(self.currentPage(), self.loaded_calibration, "Loading Calibration..."):
                self.disconnect_signals()
                with open(filename, "rb") as file_id:
                    self._model.calibration = pickle.load(file_id)
                self._calibration_passed = True
                self.next()
                self.currentPage().calibration_passed = True
                self.connect_signals()
                self.loaded_calibration.emit()

    def save(self):
        filenames = QFileDialog.getSaveFileName(self,
                                                      "Save Calibration",
                                                      os.sep.join((Settings().data_root, "saved_calibrations")),
                                                      "Calibration File (*.cal)")

        if len(filenames[0]):
            filename = filenames[0]
            with open(filename, "wb") as file_id:
                pickle.dump(self._model.calibration, file_id)
                return True
        return False

    def load_ideal(self, component_index, page=None):
        page = self.currentPage() if page is None else page
        suffix = "s1p" if component_index == 0 or component_index == len(page.component_names) - 1 else "s2p"
        filenames = QFileDialog.getOpenFileName(self,
                                                      "Load Ideal S-Parameter File",
                                                      os.sep.join((Settings().data_root, "calkits")),
                                                      "S-Parameter File (*%s)" % (suffix,))

        if len(filenames[0]):
            filename = filenames[0]
            self.set_ideal(component_index, filename)

    def set_ideal(self, component_index, filename, page=None):
        page = self.currentPage() if page is None else page
        page_name, port_nums, old_name, new_name = page.name_info(component_index, filename)
        page.ntwks[component_index] = skrf.Network(filename, name=new_name)
        ntwk = reduce(cascade, [ntwk for ntwk in page.ntwks if ntwk])
        self._model.set_ideal(page_name, port_nums, old_name, new_name, ntwk)
        if old_name == page_name:
            page.name = new_name + port_nums
        page.set_ideal(component_index, filename)

    def measure(self, page=None):
        """ Measures the calibration standard.
        """
        page = self.currentPage() if page is None else page
        page_name, port_nums, calkit_standard, _ = page.name_info()
        measure, func = self._model.measure(page_name, port_nums, calkit_standard)

        if self._model.measurement_type == "SS":
            self._runtime_view = SmallSignalRuntimeView()
        elif self._model.measurement_type == "LS":
            self._runtime_view = LargeSignalRuntimeView()
        self._runtime_thread = RuntimeThread()
        self._runtime_model = measure

        self._runtime_thread.connect_signals(self._runtime_model, self._runtime_view)
        self._runtime_thread.started_.connect(func)  # Pycharm Debugger does not work with Qthread.started
        self._runtime_thread.finished.connect(self.set_measurement)
        self._runtime_thread.finished.connect(self.save_measurement)
        self._runtime_thread.start()

    def set_measurement(self, page=None):
        """ Records the current calibration measurement.
        """
        page = self.currentPage() if page is None else page
        page_name, port_nums, calkit_standard, _ = page.name_info()
        self._model.set_measurement(page_name, port_nums, calkit_standard)

        page = self.currentPage() if page is None else page
        page.update(state=True)
        if page.optional:
            self.insert_optional_content_page()

    def save_measurement(self, page=None):
        page = self.currentPage() if page is None else page
        page_name, port_nums, calkit_standard, _ = page.name_info()
        if self._model.measurement_type == "SS":
            num_ports = len(list(filter(None, port_nums.split("_"))))
            filename = "%s%s.s%dp" % (page_name.lower().replace(" ", "_"), port_nums, num_ports)
            filenames = QFileDialog.getSaveFileName(self,
                                                          "Save S-Parameter File",
                                                          os.sep.join((Settings().data_root, "caldata", filename)),
                                                          "S-Parameter File (*.s%dp)" % (num_ports,))
        elif self._model.measurement_type == "LS":
            filename = "%s%s.mdf" % (page_name.lower().replace(" ", "_"), port_nums)
            filenames = QFileDialog.getSaveFileName(self,
                                                          "Save MDIF File",
                                                          os.sep.join((Settings().data_root, "caldata", filename)),
                                                          "MDIF File (*.mdf)")
        else:
            return

        if len(filenames[0]):
            self._model.save_measurement(filenames[0], page_name, port_nums, calkit_standard)
            return True
        return False

    def nextId(self):
        next_id = super(AbstractCalibrationWizard, self).nextId()
        if next_id > 0 and self._calibration_passed:
            return self.pageIds()[-1]
        else:
            return next_id

    def calculate(self):
        return self._model.calculate()

    def accept(self):
        self._model.apply_cal()
        self.done(QDialog.DialogCode.Accepted)

    def update(self, state=False):
        super(AbstractCalibrationWizard, self).update()
        self.currentPage().update(state=state)

