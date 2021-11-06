import os
import pickle

import numpy as np
import skrf as rf
from PySide2.QtWidgets import QFileDialog
from functools import reduce
from skrf.network import cascade

from sknrf.app.dataviewer.model.snp import SNP
from sknrf.model.sequencer.measure import Measure
from sknrf.settings import Settings
from sknrf.device.signal import ff
from sknrf.view.desktop.calibration.wizard.base import AbstractCalibrationWizard
from sknrf.view.desktop.calibration.wizard.base import AbstractPortPage, AbstractInstrumentPage, AbstractRequirementsPage
from sknrf.view.desktop.calibration.wizard.base import AbstractContentPage, AbstractConclusionPage


class ImpedancePortPage(AbstractPortPage):
    pass


class ImpedanceInstrumentPage(AbstractInstrumentPage):
    pass


class ImpedanceRequirementsPage(AbstractRequirementsPage):
    pass


class ImpedanceContentPage(AbstractContentPage):

    def isComplete(self):
        """ Defines the conditions that must be satisfied before proceeding to the the next page.
        """
        ideal_ntwks = self.wizard().model().ideal_ntwks
        measured_ntwks = self.wizard().model().measured_ntwks
        return self.optional or \
               (self.name and self.name[0] != '_' and self.name in ideal_ntwks and self.name in measured_ntwks)


class ImpedanceConclusionPage(AbstractConclusionPage):
    pass


class ImpedanceCalibrationWizard(AbstractCalibrationWizard):

    def save(self):
        filenames = list()
        filename = "impedance_calibration.cal"
        filenames = QFileDialog.getSaveFileName(self,
                                                "Save Calibration",
                                                os.sep.join((Settings().data_root, "saved_calibrations", filename)),
                                                "Calibration File (*.cal);;S-Parameter File (*.s1p)")

        if len(filenames[0]):
            filename = filenames[0]
            filename, extension = os.path.splitext(filename)
            if extension == ".cal":
                with open(filename, "wb") as file_id:
                    pickle.dump(self._model.calibration, file_id)
                    return True
            elif extension == ".s1p":
                for port_index in self.port_indices():
                    SNP.write_network(self._model.calibration[port_index],
                                      "%s_%d%s" % (filename, port_index + 1, extension))
                return True
        return False

    def set_ideal(self, component_index, filename, page=None):
        page = self.currentPage() if page is None else page
        page_name, port_nums, old_name, new_name = page.name_info(component_index, filename)
        page.ntwks[component_index] = rf.Network(filename, name=new_name)
        if old_name == page_name:
            old_name += port_nums
            new_name += port_nums
            if old_name in self._model.ideal_ntwks:
                self._model.ideal_ntwks.pop(old_name)
            if old_name in self._model.measured_ntwks:
                self._model.measured_ntwks[new_name] = self._model.measured_ntwks.pop(old_name)
                self._model.measured_ntwks[new_name].name = new_name
            self._model.ideal_ntwks[new_name] = reduce(cascade, [ntwk for ntwk in page.ntwks if ntwk])
            self._model.ideal_ntwks[new_name].name = new_name
            page.name = new_name
        else:
            self._model.ideal_ntwks[page_name + port_nums] = reduce(cascade, [ntwk for ntwk in page.ntwks if ntwk])
            self._model.ideal_ntwks[page_name + port_nums].name = page_name + port_nums
        super(ImpedanceCalibrationWizard, self).set_ideal(component_index, filename, page)

    def measure(self, page=None):
        page = self.currentPage() if page is None else page
        page_name, port_nums, _, _ = page.name_info()
        port_indices = np.array(list(filter(None, port_nums.split("_")))).astype(np.int) - 1

        self._runtime_thread.wait()
        measure = Measure(self._model.datagroup_name, page_name + port_nums)
        self._runtime_thread.set_kwargs({"port_indices": port_indices})
        self._runtime_thread.set_func(measure.single_sparameter_measurement)
        self._runtime_thread.start()
        super(ImpedanceCalibrationWizard, self).measure()

    def set_measurement(self, page=None):
        page = self.currentPage() if page is None else page
        page_name, port_nums, _, _ = page.name_info()
        num_ports = len(list(filter(None, port_nums.split("_"))))
        freq = ff.freq()
        freq = rf.Frequency.from_f(freq, unit="hz")

        dataset = self._model.datagroup_model()[self._model.datagroup_name].dataset(page.name)
        port_slice = slice(num_ports)
        s = dataset.s[...]
        s = np.asarray(s[:, :, port_slice, port_slice]).reshape((-1, num_ports, num_ports))
        network = rf.Network(name=page_name + port_nums, frequency=freq, s=s)
        self._model.measured_ntwks[page_name + port_nums] = network
        self.save_measurement()
        super(ImpedanceCalibrationWizard, self).set_measurement()

    def save_measurement(self, page=None):
        page = self.currentPage() if page is None else page
        page_name, port_nums, _, _ = page.name_info()
        network = self._model.measured_ntwks[page_name + port_nums]
        filename = "%s%s.s2p" % (page_name, port_nums)
        filenames = QFileDialog.getSaveFileName(self,
                                                "Save S-Parameter File",
                                                os.sep.join((Settings().data_root, "data", "caldata", filename)),
                                                "S-Parameter File (*.s1p)")
        if len(filenames[0]):
            filename = filenames[0]
            SNP.write_network(network,
                              os.path.dirname(filename) + os.sep + "%s%s.s2p" % (page_name, port_nums))
            return True
        return False
