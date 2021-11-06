import abc
import os
import pickle

import skrf

from sknrf.settings import Settings, InstrumentFlag
from sknrf.model.base import AbstractModel
from sknrf.model.device import DevicesModel
from sknrf.app.dataviewer.model.dataset import DatagroupModel


class CalibrationMethodTests(object, metaclass=abc.ABCMeta):

    cal_module = None
    cal_class = None
    cal_port_indices = []
    cal_measurements = [["", "", ""]]
    cal_filename = os.sep.join((Settings().data_root, "saved_calibrations", "testdata.cal"))
    calkit_dg = ""
    calkit_dg_dir = os.sep.join((Settings().data_root, "datagroups"))
    calkit_dir1 = os.sep.join((Settings().data_root, "calkits", "ideal"))
    calkit_dir2 = os.sep.join((Settings().data_root, "calkits", "ideal_ideal"))
    caldata_dir = os.sep.join((Settings().data_root, "caldata"))

    @classmethod
    def setUpClass(cls):
        pdmv = (Settings().num_ports, Settings().num_duts, Settings().num_mipi, Settings().num_video)
        AbstractModel.set_device_model(DevicesModel(*pdmv))
        AbstractModel.set_datagroup_model({cls.calkit_dg: DatagroupModel(os.sep.join((cls.calkit_dg_dir, cls.calkit_dg + ".h5")), mode="w")})
        AbstractModel.datagroup_model()[cls.calkit_dg].add("Single")

    def setUp(self):
        AbstractModel.device_model().transforms.clear()
        self.cal_model = self.cal_class()

    def test_measurement(self):
        self.cal_model.port_indices = self.cal_port_indices
        page_name, port_nums, ntwk_name = self.cal_measurements[0]
        measure, func = self.cal_model.measure(page_name, port_nums, ntwk_name)
        measure.background = True
        func()
        self.cal_model.set_measurement(page_name, port_nums, ntwk_name)

    def test_save_measurement(self):
        self.cal_model.port_indices = self.cal_port_indices
        page_name, port_nums, ntwk_name = self.cal_measurements[0]
        measure, func = self.cal_model.measure(page_name, port_nums, ntwk_name)
        measure.background = True
        func()
        self.cal_model.set_measurement(page_name, port_nums, ntwk_name)
        self.cal_model.save_measurement(self.caldata_dir, page_name, port_nums, ntwk_name)

    def test_calculate(self):
        self.cal_model.port_indices = self.cal_port_indices
        for cal_measurement in self.cal_measurements:
            page_name, port_nums, ntwk_name = cal_measurement
            num_ports = len(list(filter(None, port_nums.split("_"))))
            if num_ports == 1:
                ideal_filename = os.sep.join((self.calkit_dir1, ntwk_name + ".s1p"))
            elif num_ports == 2:
                ideal_filename = os.sep.join((self.calkit_dir2, ntwk_name + ".s2p"))
            else:
                raise ValueError("Only two-port calibration kits are supported")
            if self.cal_model.measurement_type == "SS" and os.path.isfile(ideal_filename):
                ntwk = skrf.Network(ideal_filename, name=ntwk_name)
                self.cal_model.set_ideal(page_name, port_nums, ntwk_name, ntwk_name, ntwk)
            measure, func = self.cal_model.measure(page_name, port_nums, ntwk_name)
            measure.background = True
            func()
            self.cal_model.set_measurement(page_name, port_nums, ntwk_name)
            if self.cal_model.measurement_type == "SS" and os.path.isfile(ideal_filename):
                measured_ntwk = self.cal_model.measured_ntwks[page_name + port_nums]
                self.cal_model.measured_ntwks[page_name + port_nums] = ntwk.interpolate(measured_ntwk.frequency)
        self.cal_model.calculate()

    def test_calculate_lf(self):
        self.cal_model.instrument_flags = InstrumentFlag.LF
        self.test_calculate()

    def test_calculate_rf(self):
        self.cal_model.instrument_flags = InstrumentFlag.RF
        self.test_calculate()

    def test_save(self):
        self.test_calculate()
        pickle.dump(self.cal_model, open(self.cal_filename, mode="wb"))

    def test_load(self):
        self.test_save()
        cal_model = pickle.load(open(self.cal_filename, mode="rb"))

    def test_apply(self):
        self.test_calculate()
        self.cal_model.apply_cal()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        AbstractModel._datagroup_model[cls.calkit_dg].close()
