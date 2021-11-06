import os
import sys
import webbrowser

from PySide2.QtWidgets import QMainWindow, QFrame, QWidget
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy

from sknrf.widget.propertybrowser.view.enums import DISPLAY
from sknrf.view.desktop.settings.QSettings import Ui_settings
from sknrf.view.desktop.settings.QSettingsView import Ui_settingsView
from sknrf.settings import Settings, DeviceFlag, device_name_map
from sknrf.utilities.numeric import str2num, num2str, scale_map

from sknrf.widget.propertybrowser.view import BrowserCol, QtBrowserItem

__author__ = 'dtbespal'


class SettingsFrame(QFrame, Ui_settings):
    """Global Settings() sideview frame

        A frame that displays global settings that must be specified before performing calibration.

        Keyword Args:
            parent (QWidget): Parent GUI container
    """

    def __init__(self, parent=None):
        super(SettingsFrame, self).__init__(parent)
        self.setupUi(self)
        self.triggerDeviceComboBox.addItems(list(device_name_map.values()))
        self.connect_signals()
        self.update()

    def connect_signals(self):
        self.f0LineEdit.returnPressed.connect(self.set_f0)
        self.numHarmonicsLineEdit.returnPressed.connect(self.set_num_harmonics)
        self.fPointsLineEdit.returnPressed.connect(self.set_f_points)

        self.tStepLineEdit.returnPressed.connect(self.set_t_step)
        self.tStopLineEdit.returnPressed.connect(self.set_t_stop)
        self.tPointsLineEdit.returnPressed.connect(self.set_t_points)

        self.triggerDeviceComboBox.currentIndexChanged.connect(self.set_trigger_device)
        self.triggerPortSpinBox.valueChanged.connect(self.set_trigger_port)

        self.datagroupLineEdit.editingFinished.connect(self.set_datagroup)
        self.datasetLineEdit.editingFinished.connect(self.set_dataset)

        self.f0LineEdit.editingFinished.connect(self.update)
        self.numHarmonicsLineEdit.editingFinished.connect(self.update)
        self.fPointsLineEdit.editingFinished.connect(self.update)

        self.tStepLineEdit.editingFinished.connect(self.update)
        self.tStopLineEdit.editingFinished.connect(self.update)
        self.tPointsLineEdit.editingFinished.connect(self.update)

        self.datagroupLineEdit.editingFinished.connect(self.update)
        self.datasetLineEdit.editingFinished.connect(self.update)

    def disconnect_signals(self):
        self.f0LineEdit.returnPressed.disconnect(self.set_f0)
        self.numHarmonicsLineEdit.returnPressed.disconnect(self.set_num_harmonics)
        self.fPointsLineEdit.returnPressed.disconnect(self.set_f_points)

        self.tStepLineEdit.returnPressed.disconnect(self.set_t_step)
        self.tStopLineEdit.returnPressed.disconnect(self.set_t_stop)
        self.tPointsLineEdit.returnPressed.disconnect(self.set_t_points)

        self.triggerDeviceComboBox.valueChanged.disconnect(self.set_trigger_device)
        self.triggerPortSpinBox.valueChanged.disconnect(self.set_trigger_port)

        self.datagroupLineEdit.editingFinished.disconnect(self.set_datagroup)
        self.datasetLineEdit.editingFinished.disconnect(self.set_dataset)

        self.f0LineEdit.editingFinished.disconnect(self.update)
        self.numHarmonicsLineEdit.editingFinished.disconnect(self.update)
        self.fPointsLineEdit.editingFinished.disconnect(self.update)

        self.tStepLineEdit.editingFinished.disconnect(self.update)
        self.tStopLineEdit.editingFinished.disconnect(self.update)
        self.tPointsLineEdit.editingFinished.disconnect(self.update)

        self.datagroupLineEdit.editingFinished.disconnect(self.update)
        self.datasetLineEdit.editingFinished.disconnect(self.update)

    def set_f0(self, f0=None):
        if not f0:
            f0 = str2num(self.f0LineEdit.text())
        Settings().f0 = f0
        self.update(freq=True)

    def set_num_harmonics(self, num_harmonics=None):
        if not num_harmonics:
            num_harmonics = str2num(self.numHarmonicsLineEdit.text())
        Settings().num_harmonics = num_harmonics
        self.update(freq=True)

    def set_f_points(self, f_points=None):
        if not f_points:
            f_points = str2num(self.fPointsLineEdit.text())
        Settings().f_points = f_points
        self.update(freq=True)

    def set_t_step(self, t_step=None):
        if not t_step:
            t_step = str2num(self.tStepLineEdit.text())
        Settings().t_step = t_step
        self.update(time=True)

    def set_t_stop(self, t_stop=None):
        if not t_stop:
            t_stop = str2num(self.tStopLineEdit.text())
        Settings().t_stop = t_stop
        self.update(time=True)

    def set_t_points(self, t_points=None):
        if not t_points:
            t_points = str2num(self.tPointsLineEdit.text())
        Settings().t_points = t_points
        self.update(time=True)

    def set_trigger_device(self, trigger_index):
        Settings().trigger_device = DeviceFlag(1 << trigger_index)
        self.update(trigger=True)

    def set_trigger_port(self, trigger_port):
        Settings().trigger_port = trigger_port
        self.update(trigger=True)

    def set_datagroup(self, datagroup=None):
        if not datagroup:
            datagroup = self.datagroupLineEdit.text()
        Settings().datagroup = datagroup
        self.update(dataset=True)

    def set_dataset(self, dataset=None):
        if not dataset:
            dataset = self.datasetLineEdit.text()
        Settings().dataset = dataset
        self.update(dataset=True)

    def update(self, freq=False, time=False, trigger=False, dataset=False):
        super(SettingsFrame, self).update()
        all_ = not(freq or time or trigger or dataset)

        if freq or all_:
            self.f0LineEdit.setText(num2str(Settings().f0))
            self.numHarmonicsLineEdit.setText(num2str(Settings().num_harmonics))
            self.fPointsLineEdit.setText(num2str(Settings().f_points))

        if time or all_:
            self.tStepLineEdit.setText(num2str(Settings().t_step))
            self.tStopLineEdit.setText(num2str(Settings().t_stop))
            self.tPointsLineEdit.setText(num2str(Settings().t_points))

        if trigger or all_:
            device_index, device_value = 0, Settings().trigger_device.value
            while 1 << device_index != device_value:
                device_index += 1
            self.triggerDeviceComboBox.setCurrentIndex(device_index)
            self.triggerPortSpinBox.setEnabled((Settings().trigger_device & DeviceFlag.INSTRUMENT).value > 0)
            self.triggerPortSpinBox.setRange(1, Settings().num_ports)
            self.triggerPortSpinBox.setValue(int(Settings().trigger_port))

        if dataset or all:
            self.datagroupLineEdit.setText(Settings().datagroup)
            self.datasetLineEdit.setText(Settings().dataset)


class SettingsView(QMainWindow, Ui_settingsView):
    """Global Settings() Menu

        Keyword Args:
            parent (QWidget): Parent GUI container
    """
    def __init__(self, parent=None, model=None):
        super(SettingsView, self).__init__(parent)
        self.setupUi(self)

        self.settings_frame = SettingsFrame(self.mainTab)
        vbl = QVBoxLayout()
        vbl.setContentsMargins(0, 0, 0, 0)
        vbl.setSpacing(0)
        vbl.addWidget(self.settings_frame)
        self.mainTab.setLayout(vbl)
        self.tabWidget.removeTab(2)  # Remove App Tab by default

        self._model = model
        self.connect_signals()
        self.propertyTable.property_browser.display = DISPLAY.PUBLIC
        self.propertyTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.FORMAT])
        self.propertyTable.property_browser.set_update(self.update,
                                                               **{"time": True, "freq": True, "dataset": True,
                                                                  "settings": True})
        self.appPropertyTable.property_browser.display = DISPLAY.PUBLIC
        self.appPropertyTable.property_browser.setAttributes([BrowserCol.UNIT, BrowserCol.FORMAT])
        self.appPropertyTable.property_browser.set_update(self.update,
                                                               **{"time": True, "freq": True, "dataset": True,
                                                                  "app": True})
        self.set_model(Settings())

    def connect_signals(self):
        self.actionDocumentation.triggered.connect(self.clicked_doc)
        self.buttonBox.accepted.connect(self.accept)

    def disconnect_signals(self):
        self.actionDocumentation.triggered.disconnect()
        self.buttonBox.accepted.disconnect()

    def model(self):
        return self._model

    def set_model(self, model):
        self.disconnect_signals()
        self._model = model
        property_browser = self.propertyTable.property_browser
        property_browser.set_model(Settings())

        if model and not isinstance(model, Settings):
            self._model = model
            self.appPropertyTable.property_browser.set_model(self._model)
            self.tabWidget.addTab(self.appTab, "App")
        self.connect_signals()

    def clicked_doc(self):
        name = self.__module__
        if name == '__main__':
            filename = sys.modules[self.__module__].__file__
            name = filename[len(Settings().root)::].replace(".py", "").replace(os.sep, ".")
        url = Settings().url_root + Settings().url_api + name + ".html"
        webbrowser.open(url, new=2, autoraise=True)

    def update(self, freq=False, time=False, dataset=False, settings=False, app=False):
        value = (freq or time or dataset or settings or app)
        all_ = not(freq or time or dataset or value)

        self.settings_frame.update(freq=freq, time=time, dataset=dataset)
        if value or all_:
            self.propertyTable.property_browser.render()
        if value or all_:
            self.appPropertyTable.property_browser.render()

    def accept(self):
        self.close()
