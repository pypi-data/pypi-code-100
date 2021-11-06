import unittest
import os
import sys
import pickle

from sknrf.settings import Settings
from sknrf.enums.sequencer import Sweep
from sknrf.model.device import DevicesModel
from sknrf.model.base import AbstractModel
from sknrf.app.dataviewer.model.dataset import DatagroupModel
from sknrf.model.sequencer.sweep.real import LinearSweep, LogSweep
from sknrf.model.sequencer.sweep.frequency import FundLOSpanSweep, FundSSBSpanSweep, FundDSBSpanSweep, FundPhasorSpanSweep
from sknrf.model.sequencer.measure import Measure
from sknrf.utilities.numeric import Info

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'

root = os.sep.join((Settings().root, "model", "sequencer", "tests"))
dg_dir = os.sep.join((Settings().data_root, "datagroups"))
dirname = os.sep.join((Settings().data_root, "testdata"))


class TestMeasureSaveLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init_test(cls.__name__)

    def setUp(self):
        self.measure = Measure()
        self.measure.background = True

    def test_save(self):
        filename = os.sep.join((dirname, "saved_state.p"))
        with open(filename, "wb") as file_id:
            pickle.dump(Settings(), file_id)
            pickle.dump(AbstractModel.device_model(), file_id)
            pickle.dump(self.measure, file_id)

    def test_load(self):
        self.test_save()
        filename = os.sep.join((dirname, "saved_state.p"))
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(filename, "rb") as file_id:
            Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))
            AbstractModel.device_model().disconnect_handles()
            AbstractModel.set_device_model(pickle.load(file_id))
            measure = pickle.load(file_id)
            self.assertIsInstance(measure, Measure)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()


class TestSingle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init_test(cls.__name__)

    def setUp(self):
        self.measure = Measure()
        self.measure.background = True

    def test_single(self):
        Settings().dataset = "test_single2"
        self.measure.single_measurement((), {})

    def test_sparameter(self):
        Settings().dataset = "test_sparameter"
        self.measure.single_sparameter_measurement((), {})

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()


class TestSweep(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init_test(cls.__name__)

    def setUp(self):
        self.measure = Measure()
        self.sweep1 = LinearSweep(False, 0.0, 5.0, 1.0, 0)
        self.sweep2 = LogSweep(False, 20, 1, 11)
        self.measure.background = True

    def test_sweep_1(self):
        Settings().dataset = "test_sweep_1"
        self.measure.add_sweep(Sweep.V_SET, 1, 0, self.sweep1)
        self.measure.realtime = False
        self.measure.swept_measurement((), {})

    def test_sweep_1_realtime(self):
        Settings().dataset = "test_sweep_1_realtime"
        self.sweep1.realtime = True
        self.measure.add_sweep(Sweep.V_SET, 1, 0, self.sweep1)
        self.measure.realtime = True
        self.measure.swept_measurement((), {})

    def test_sweep_2(self):
        Settings().dataset = "test_sweep_2"
        self.measure.add_sweep(Sweep.V_SET, 1, 0, self.sweep1)
        self.measure.add_sweep(Sweep.A_SET, 1, 1, self.sweep2)
        self.measure.realtime = False
        self.measure.swept_measurement((), {})

    def test_sweep_2_realtime(self):
        Settings().dataset = "test_sweep_2_realtime"
        self.sweep1.realtime, self.sweep2.realtime = True, True
        self.measure.add_sweep(Sweep.V_SET, 1, 0, self.sweep1)
        self.measure.add_sweep(Sweep.A_SET, 1, 1, self.sweep2)
        self.measure.realtime = True
        self.measure.swept_measurement((), {})

    def test_sweep_2_mixed(self):
        Settings().dataset = "test_sweep_2_mixed"
        self.sweep1.realtime, self.sweep2.realtime = True, False
        self.measure.add_sweep(Sweep.V_SET, 1, 0, self.sweep1)
        self.measure.add_sweep(Sweep.A_SET, 1, 1, self.sweep2)
        self.measure.realtime = True
        self.measure.swept_measurement((), {})

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()


class TestSweepSParameter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init_test(cls.__name__)

    def setUp(self):
        Settings().ss_num_ports = 2
        Settings().ss_power = 0.001  # -30 dBm
        Settings().ss_f0 = Settings().f0
        Settings().ss_span = 1
        Settings().ss_points = Settings().t_points
        Settings().ss_harm = "all"
        Settings().ss_ref = "response"
        Settings().ss_mod = "dsb"  # complex: phasor, real: dsb
        Settings().ss_realtime = False

        self.measure = Measure()
        self.sweep1 = LinearSweep(False, 0.0, 5.0, 1.0, 0)
        self.sweep2 = LogSweep(False, 20, 1, 11)
        self.measure.background = True

    def test_sweep_fund_lo(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_lo"
        freq_sweep = FundLOSpanSweep(False, Settings().f0, 1/Settings().t_step, points=3)
        self.measure.add_sweep(Sweep.LO, sweep_plan=freq_sweep)
        self.measure.realtime = False
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_ssb(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_ssb"
        freq_sweep = FundSSBSpanSweep(False, Settings().f0, 1/Settings().t_step, points=3)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.realtime = False
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_ssb_filter(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_ssb_filter"
        freq_sweep = FundSSBSpanSweep(False, Settings().f0, 1 / Settings().t_step, points=3, level=True)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.realtime = False
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_ssb_all(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_ssb_all"
        freq_sweep = FundSSBSpanSweep(False, Settings().f0, 1/Settings().t_step, points=3, all_=True)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.realtime = False
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_dsb(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_dsb"
        Settings().ss_mod = "dsb"
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_dsb_ss_ref(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_dsb_ss_ref"
        Settings().ss_ref = "stimulus"
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_dsb_ss_harm(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_dsb_ss_harm_lf"
        Settings().ss_harm = "lf"
        self.measure.realtime = False
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * 1, num_ports + 1, num_ports + 1))
        Settings().dataset = "test_sweep_fund_dsb_ss_harm_rf"
        Settings().ss_harm = "rf"
        self.measure.realtime = False
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().num_harmonics, num_ports + 1, num_ports + 1))

    def test_sweep_fund_dsb_ss_realtime(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_dsb_ss_harm_realtime"
        Settings().ss_realtime = True
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_dsb_filter(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_dsb_filter"
        Settings().realtime = True
        freq_sweep = FundDSBSpanSweep(False, Settings().f0, 1 / Settings().t_step, points=3, level=True)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_dsb_all(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_dsb_all"
        Settings().realtime = True
        freq_sweep = FundDSBSpanSweep(False, Settings().f0, 1/Settings().t_step, points=3, all_=True)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_phasor(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_phasor"
        freq_sweep = FundDSBSpanSweep(False, Settings().f0, 1/Settings().t_step, points=3)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_phasor_filter(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_phasor_filter"
        freq_sweep = FundDSBSpanSweep(False, Settings().f0, 1 / Settings().t_step, points=3, level=True)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def test_sweep_fund_phasor_all(self):
        num_ports = Settings().num_ports
        Settings().dataset = "test_sweep_fund_phasor_all"
        Settings().realtime = True
        freq_sweep = FundDSBSpanSweep(False, Settings().f0, 1/Settings().t_step, points=3, all_=True)
        self.measure.add_sweep(Sweep.SP_FUND, sweep_plan=freq_sweep)
        self.measure.single_sparameter_measurement((), {})
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        self.assertEqual(ds.s[...].shape, (Settings().ss_points * Settings().f_points, num_ports + 1, num_ports + 1))

    def tearDown(self):
        Settings().ss_num_ports = 2
        Settings().ss_power = 0.001  # -30 dBm
        Settings().ss_f0 = Settings().f0
        Settings().ss_span = 1
        Settings().ss_points = Settings().t_points
        Settings().ss_harm = "all"
        Settings().ss_ref = "response"
        Settings().ss_mod = "dsb"  # complex: phasor, real: dsb
        Settings().ss_realtime = False

    @classmethod
    def tearDownClass(cls):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()


class TestSweepMisc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init_test(cls.__name__)

    def setUp(self):
        self.measure = Measure()
        self.sweep1 = LinearSweep(False, 0.0, 5.0, 1.0, 0)
        self.sweep2 = LogSweep(False, 20, 1, 11)
        self.measure.background = True

    @unittest.skip  # todo: fix tensor.copy_ for complex
    def test_sweep_phase(self):
        Settings().dataset = "test_sweep_phase"
        phase_sweep = LinearSweep(False, 0., 360., points=18)
        self.measure.add_sweep(Sweep.PHASE, 1, 1, phase_sweep)
        self.measure.realtime = False
        self.measure.swept_measurement((), {})

    def test_sweep_tau(self):
        Settings().dataset = "test_sweep_tau"
        phase_sweep = LinearSweep(False, 0., 10*Settings().t_step, points=11)
        self.measure.add_sweep(Sweep.TAU, 1, 1, phase_sweep)
        self.measure.realtime = False
        self.measure.swept_measurement((), {})

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()


def iterator_test_suite():
    from sknrf.model.tests.test_device import TestDeviceSaveLoad, TestDeviceConnections
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceSaveLoad))
    test_suite.addTest(unittest.makeSuite(TestDeviceConnections))
    test_suite.addTest(unittest.makeSuite(TestSingle))
    test_suite.addTest(unittest.makeSuite(TestSweep))
    test_suite.addTest(unittest.makeSuite(TestSweepSParameter))
    test_suite.addTest(unittest.makeSuite(TestSweepMisc))

    return test_suite


if __name__ == '__main__':
    pass
    # import sys
    # from PySide import QtCore
    # from sknrf.model.base import AbstractModel
    #
    # app = QtCore.QCoreApplication(sys.argv)
    # AbstractModel.init()
    #
    # runner = unittest.TextTestRunner()
    # runner.run(iterator_test_suite())
