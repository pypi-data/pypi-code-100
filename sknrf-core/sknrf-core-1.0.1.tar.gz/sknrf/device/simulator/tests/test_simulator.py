import unittest

import numpy as np
import os
from numpy.testing import *

from sknrf.settings import Settings
from sknrf.device.simulator.keysight import ads


class TestADSConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Settings().f0 = 1e9
        Settings().num_harmonics = 3
        Settings().t_stop = 100e-9
        Settings().t_step = 10e-9

        cls.remote_host = Settings().remote_host
        cls.remote_user = Settings().remote_user
        cls.remote_password = Settings().remote_password
        cls.remote_key_filename = Settings().remote_key_filename
        # cls.remote_host = ""
        # cls.remote_user = ""
        # cls.remote_key_file = None
        cls.netlist_filename = os.sep.join((Settings().root(), "device", "simulator", "keysight",
                                            "ADSSimulatorxUnitTest_wrk", "ads_unit_test_netlist.txt"))
        cls.dataset_filename = os.sep.join((Settings().root(), "device", "simulator", "keysight",
                                            "ADSSimulatorxUnitTest_wrk", "data", "ads_unit_test_dataset.mat"))
        cls.config_filename = os.sep.join((Settings().root(), "device", "simulator", "keysight",
                                           "ADSSimulatorxUnitTest_wrk", "hpeesofsim.cfg"))
        cls.bad_netlist_filename = "bad_ads_unit_test_netlist.txt"
        cls.bad_dataset_filename = "bad_ads_unit_test_dataset.mat"
        cls.default_simulation_type = "DC"
        cls.default_simulation_name = "DC1"
        cls.simulator = None

    def test_connect_simulator(self):
        self.simulator = ads.ADSSimulator(self.netlist_filename, self.dataset_filename,
                                          self.default_simulation_type, self.default_simulation_name,
                                          remote_host=self.remote_host, remote_user=self.remote_user,
                                          remote_password=self.remote_password, remote_key_filename=self.remote_key_filename,
                                          remote_port=2222)
        self.assertIsInstance(self.simulator, ads.ADSSimulator)

    def test_preset(self):
        self.simulator = ads.ADSSimulator(self.netlist_filename, self.dataset_filename,
                                          self.default_simulation_type, self.default_simulation_name,
                                          remote_host=self.remote_host, remote_user=self.remote_user,
                                          remote_password=self.remote_password, remote_key_filename=self.remote_key_filename,
                                          remote_port=2222)
        self.simulator.preset()

    def tearDown(self):
        pass


class TestADSSingle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Settings().f0 = 1e9
        Settings().num_harmonics = 3
        Settings().t_stop = 100e-9
        Settings().t_step = 10e-9

        cls.remote_host = Settings().remote_host
        cls.remote_user = Settings().remote_user
        cls.remote_password = Settings().remote_password
        cls.remote_key_filename = Settings().remote_key_filename
        # cls.remote_host = ""
        # cls.remote_user = ""
        # cls.remote_key_file = None
        cls.netlist_filename = os.sep.join((Settings().root(), "device", "simulator", "keysight",
                                            "ADSSimulatorxUnitTest_wrk", "ads_unit_test_netlist.txt"))
        cls.dataset_filename = os.sep.join((Settings().root(), "device", "simulator", "keysight",
                                            "ADSSimulatorxUnitTest_wrk", "data", "ads_unit_test_dataset.mat"))
        cls.config_filename = os.sep.join((Settings().root(), "device", "simulator", "keysight",
                                           "ADSSimulatorxUnitTest_wrk", "hpeesofsim.cfg"))
        cls.bad_netlist_filename = "bad_ads_unit_test_netlist.txt"
        cls.bad_dataset_filename = "bad_ads_unit_test_dataset.mat"
        cls.default_simulation_type = "DC"
        cls.default_simulation_name = "DC1"

    def setUp(self):
        self.simulator = ads.ADSSimulator(self.netlist_filename, self.dataset_filename,
                                          self.default_simulation_type, self.default_simulation_name,
                                          remote_host=self.remote_host, remote_user=self.remote_user,
                                          remote_password=self.remote_password, remote_key_filename=self.remote_key_filename,
                                          remote_port=2222)

    def test_read_netlist_numeric(self):
        self.assertAlmostEqual(self.simulator.read_netlist("NumericVar1"), 42e-4, 3)

    def test_read_netlist_numeric_array(self):
        arr = np.array([1, 2+1.00j, 3.00], dtype=np.complex128)
        assert_allclose(self.simulator.read_netlist("NumericArray1"), arr)

    def test_read_netlist_string(self):
        self.assertEqual(self.simulator.read_netlist("StringVar1"), "pass")

    def test_read_netlist_filename(self):
        self.assertEqual(self.simulator.read_netlist("FilenameVar1"), r"\usr\bin")

    def test_read_netlist_unknown(self):
        with self.assertRaises(AttributeError):
            self.simulator.read_netlist("UnknownVar")

    def test_read_netlist_block(self):
        self.assertAlmostEqual(self.simulator.read_netlist("Block1.Vdc"), 21, 3)

    def test_write(self):
        self.simulator.write("NumericVar1", 25)

    def test_write_numeric(self):
        self.simulator.write("NumericVar1", 25)
        self.assertAlmostEqual(self.simulator.read_netlist("NumericVar1"), 25, 3)

    def test_write_numeric_array(self):
        arr = np.array([1.00, 2.00+3j, 43.231])
        self.simulator.write("NumericArray1", arr)
        assert_allclose(self.simulator.read_netlist("NumericArray1"), arr)

    def test_write_string(self):
        self.simulator.write("StringVar1", "failed")
        self.assertEqual(self.simulator.read_netlist("StringVar1"), "failed")

    def test_write_filename(self):
        self.simulator.write("FilenameVar1", r"\usr\local\bin")
        self.assertEqual(self.simulator.read_netlist("FilenameVar1"), r"\usr\local\bin")

    def test_write_unknown(self):
        with self.assertRaises(AttributeError):
            self.simulator.write("UnknownVar", 1)

    def test_write_block(self):
        self.simulator.write("Block1.Vdc", 123e-5)
        self.assertAlmostEqual(self.simulator.read_netlist("Block1.Vdc"), 123e-5, 3)

    def test_measure(self):
        result, log = self.simulator.measure()
        self.assertEqual(result, 0)

    def test_read_dc_dataset(self):
        self.simulator.simulator_type = 'DC'
        self.simulator.simulator_name = 'DC1'
        assert_array_almost_equal(self.simulator.read('Meas1'), np.array([[[21]]]), 3)

    def test_read_harmonic_balance_dataset(self):
        self.simulator.simulator_type = 'HB'
        self.simulator.simulator_name = 'HB1'
        expected_value = np.array([21, 0, 0, 0, 0, 0]).reshape((1, -1, 1))
        assert_array_almost_equal(self.simulator.read('Meas1'), expected_value, 3)

    def test_read_envelope_dataset(self):
        self.simulator.simulator_type = 'Env1.HB'
        self.simulator.simulator_name = 'Env1'
        expected_value = np.tile(np.array([21, 0, 0, 0, 0, 0]).reshape((1, -1, 1)), (1, 1, 11))
        assert_array_almost_equal(self.simulator.read('Meas1'), expected_value, 3)

    def test_write_measure_read(self):
        self.simulator.write("Block1.Vdc", 42)
        self.simulator.measure()
        result = np.zeros((1, 1, 1), dtype=np.complex128)
        result[0, 0, 0] = 42
        assert_array_almost_equal(self.simulator.read('Meas1'), result, 3)

    def tearDown(self):
        self.simulator.preset()


if __name__ == '__main__':
    unittest.main()
