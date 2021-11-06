import unittest
import os
import pickle

from sknrf.enums.runtime import Bound
from sknrf.enums.modulation import POWER_CLASS, CA, DF_OOB, TECH, MOD
from sknrf.enums.modulation import LTE_BAND, LTE_BW, LTE_RB
from sknrf.enums.modulation import WCDMA_BAND, WCDMA_BW, WCDMA_RB
from sknrf.enums.modulation import CDMA_BAND, CDMA_BW, CDMA_RB
from sknrf.enums.modulation import GSM_BAND, GSM_BW, GSM_RB
from sknrf.settings import Settings, DeviceFlag

root = os.sep.join((Settings().root, "device", "tests"))
dirname = os.sep.join((Settings().data_root, "testdata"))


class TestSettingSaveLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_save(self):
        filename = os.sep.join((dirname, "saved_state.p"))
        with open(filename, "wb") as file_id:
            pickle.dump(Settings(), file_id)

    def test_load(self):
        self.test_save()
        filename = os.sep.join((dirname, "saved_state.p"))
        with open(filename, "rb") as file_id:
            Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))

    def tearDown(self):
        pass


class TestSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass
        # import sys
        # from PySide2 import QtCore
        # cls.app = QtCore.QCoreApplication(sys.argv)

    def setUp(self):
        Settings().blockSignals(True)

    def test_read_general_settings(self):
        self.assertIsInstance(Settings().num_ports, int)
        self.assertIsInstance(Settings().num_duts, int)
        self.assertIsInstance(Settings().num_mipi, int)
        self.assertIsInstance(Settings().num_video, int)
        self.assertIsInstance(Settings().precision, int)
        self.assertIsInstance(Settings().bound, Bound)

    def test_write_general_settings(self):
        Settings().num_ports = 1
        Settings().num_duts = 1
        Settings().num_mipi = 1
        Settings().num_video = 1
        Settings().precision = 3
        Settings().bound = Bound.OFF

    def test_read_display_settings(self):
        self.assertIsInstance(Settings().color_map, dict)
        self.assertIsInstance(Settings().color_order, list)
        self.assertIsInstance(Settings().line_order, list)
        self.assertIsInstance(Settings().marker_order, list)

    def test_write_display_settings(self):
        pass
        # self.assertRaises(AttributeError, Settings().color_map.fset({}))
        # self.assertRaises(AttributeError, Settings().color_order.fset([]))
        # self.assertRaises(AttributeError, Settings().line_order.fset([]))
        # self.assertRaises(AttributeError, Settings().marker_order.fset([]))

    def test_read_rf_settings(self):
        Settings().t_step = 1e-6
        Settings().t_stop = 10e-6
        Settings().t_rise = 1e-6
        Settings().t_settle = 1e-6
        Settings().t_fall = 1e-6
        Settings().f0 = 1e9
        Settings().num_harmonics = 3
        Settings().trigger_port = 1
        Settings().trigger_device = DeviceFlag.RFRECEIVER
        Settings().z0 = 50.0

    def test_write_rf_settings(self):
        self.assertIsInstance(Settings().t_step, float)
        self.assertIsInstance(Settings().t_stop, float)
        self.assertIsInstance(Settings().t_rise, float)
        self.assertIsInstance(Settings().t_settle, float)
        self.assertIsInstance(Settings().t_fall, float)
        self.assertIsInstance(Settings().f0, float)
        self.assertIsInstance(Settings().num_harmonics, int)
        self.assertIsInstance(Settings().trigger_port, int)
        self.assertIsInstance(Settings().trigger_device.value, int)
        self.assertIsInstance(Settings().z0, float)

    def test_read_dsp_settings(self):
        self.assertIsInstance(Settings().lock_lo, bool)

    def test_write_dsp_settings(self):
        Settings().lock_lo = False

    def test_read_aux_settings(self):
        self.assertIsInstance(Settings().ss_num_ports, int)
        self.assertIsInstance(Settings().ss_power, float)
        self.assertIsInstance(Settings().ss_f0, float)
        self.assertIsInstance(Settings().ss_span, float)
        self.assertIsInstance(Settings().ss_points, int)

    def test_write_aux_settings(self):
        Settings().ss_num_ports = 2
        Settings().ss_power = 0.001
        Settings().ss_f0 = 1.0e9
        Settings().ss_span = 100e6
        Settings().ss_points = 500

    def test_read_video_settings(self):
        self.assertIsInstance(Settings().v_cols, int)
        self.assertIsInstance(Settings().v_rows, int)

    def test_write_video_settings(self):
        Settings().v_cols = 32
        Settings().v_rows = 32

    def test_read_iteration_settings(self):
        self.assertIsInstance(Settings().realtime, bool)
        self.assertIsInstance(Settings().sweep_avg, int)
        self.assertIsInstance(Settings().signal_avg, int)
        self.assertIsInstance(Settings().sweep_rep, int)
        self.assertIsInstance(Settings().signal_rep, int)
        self.assertIsInstance(Settings().max_iter, int)

    def test_write_iteration_settings(self):
        Settings().realtime = False
        Settings().sweep_avg = 1
        Settings().signal_avg = 1
        Settings().sweep_rep = 1
        # Settings().signal_rep = 1
        Settings().max_iter = 100

    def test_read_database_settings(self):
        self.assertIsInstance(Settings().environment, str)
        self.assertIsInstance(Settings().root, str)
        self.assertIsInstance(Settings().data_root, str)
        self.assertIsInstance(Settings().url_root, str)
        self.assertIsInstance(Settings().url_api, str)
        self.assertIsInstance(Settings().datagroup, str)
        self.assertIsInstance(Settings().dataset, str)

    def test_write_database_settings(self):
        # Settings().environment = "py36"
        Settings().root = "../sknrf"
        Settings().data_root = "../sknrf/data"
        Settings().url_root = "../doc/build/html"
        Settings().url_api = "internal/api"
        Settings().datagroup = "Single"
        Settings().dataset = "Single"

    def test_read_simulation_on_off_order(self):
        self.assertIsInstance(Settings().off_order, list)
        self.assertIsInstance(Settings().on_order, list)
        self.assertIsInstance(Settings().ss_on_order, list)
        self.assertIsInstance(Settings().ss_off_order, list)

    def test_write_simulation_on_off_order(self):
        Settings().off_order = []
        Settings().on_order = []
        Settings().ss_on_order = []
        Settings().ss_off_order = []

    def test_read_simulation_settings(self):
        self.assertIsInstance(Settings().netlist_filename, str)
        self.assertIsInstance(Settings().dataset_filename, str)
        self.assertIsInstance(Settings().remote_host, str)
        self.assertIsInstance(Settings().remote_user, str)
        self.assertIsInstance(Settings().remote_password, str)
        self.assertIsInstance(Settings().remote_key_filename, str)
        self.assertIsInstance(Settings().remote_port, int)

    def test_write_simulation_settings(self):
        Settings().netlist_filename = "netlist.txt"
        Settings().dataset_filename = "dataset.mat"
        Settings().remote_host = "127.0.0.1"
        Settings().remote_user = "user"
        Settings().remote_password = "password"
        Settings().remote_key_filename = "./.ssh/rsa"
        Settings().remote_port = 2222

    def tearDown(self):
        Settings().blockSignals(False)
        Settings().load()
