import unittest
import os

import numpy as np
import torch as th
from numpy.testing import *
from collections import OrderedDict
import tables as tb

from sknrf.settings import Settings
from sknrf.app.dataviewer.model.dataset import DatagroupModel, DatasetModel, IQFile
from sknrf.app.dataviewer.model.equation import DatasetEquationModel

__author__ = 'dtbespal'

root = os.sep.join((Settings().data_root, "testdata", "dataset"))


class Test_IQFileBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.iq_array = np.asarray([-32767 + 1j*32767, -1 + 1j*1], dtype=np.complex)
        cls.iq_string = b'\x80\x01\x7f\xff\xff\xff\x00\x01'
        cls.header_map = {"sample_point": 307200,
                          "sample_rate": 30.72e6,
                          "waveform_runtime_scaling": 0.864,
                          "iq_modulation_filter": 40e6,
                          "iq_output_filter": 40e6,
                          "marker_1": "1-307",
                          "marker_2": None,
                          "marker_3": "61451-153590, 215051-307190",
                          "marker_4": "1-44, 61397-153644, 214997-307200",
                          "pulse__rf_blanking": 4,
                          "alc_hold": 3,
                          "alc_status": "On",
                          "bandwidth": "Auto",
                          "power_search_reference": "Modulation"}
        cls.marker_array = np.zeros((Settings().t_points,), dtype=">i1")
        cls.marker_array[0:307] |= np.left_shift(1, 1 - 1)
        cls.marker_array[61450:153590] |= np.left_shift(1, 3 - 1)
        cls.marker_array[215050:307190] |= np.left_shift(1, 3 - 1)
        cls.marker_array[0:44] |= np.left_shift(1, 4 - 1)
        cls.marker_array[61396:153644] |= np.left_shift(1, 4 - 1)
        cls.marker_array[214996:307200] |= np.left_shift(1, 4 - 1)

        cls.filename_read = root + os.sep + "iq_read.h5"
        cls.filename_write = root + os.sep + "iq_write.h5"

        cls.i_filename_read = root + os.sep + "i_read.txt"
        cls.i_filename_write = root + os.sep + "i_write.txt"
        cls.q_filename_read = root + os.sep + "q_read.txt"
        cls.q_filename_write = root + os.sep + "q_write.txt"
        cls.config_filename_read = root + os.sep + "config_read.txt"
        cls.config_filename_write = root + os.sep + "config_write.txt"

        cls.iq_filename_read = root + os.sep + "waveform" + os.sep + "read"
        cls.iq_filename_write = root + os.sep + "waveform" + os.sep + "write"
        cls.header_filename_read = root + os.sep + "header" + os.sep + "read"
        cls.header_filename_write = root + os.sep + "header" + os.sep + "write"
        cls.marker_filename_read = root + os.sep + "marker" + os.sep + "read"
        cls.marker_filename_write = root + os.sep + "marker" + os.sep + "write"

    def setUp(self):
        self.iq_file = None

    def test_create_iq_file(self):
        self.iq_file = IQFile(self.filename_write, mode='w')
        self.assertTrue(isinstance(self.iq_file.iq, th.Tensor))
        self.assertTrue(isinstance(self.iq_file.header, OrderedDict))
        self.assertTrue(isinstance(self.iq_file.marker, th.Tensor))

    def test_from_waveform(self):
        self.iq_file = IQFile.from_waveform(self.filename_write, self.iq_array, self.header_map)
        self.assertTupleEqual((Settings().t_points,), self.iq_file.iq.shape)
        self.assertGreater(len(self.iq_file.header), 0)
        self.assertTupleEqual((Settings().t_points,), self.iq_file.marker.shape)

    def test_to_waveform_type(self):
        self.iq_file = IQFile(self.filename_read, mode='r')
        iq, header, marker = self.iq_file.to_waveform()

        self.assertTrue(isinstance(iq, np.ndarray))
        self.assertTrue(isinstance(header, OrderedDict))
        self.assertTrue(isinstance(marker, np.ndarray))

    def test_to_waveform_shape(self):
        self.iq_file = IQFile(self.filename_read, mode='r')
        iq, header, marker = self.iq_file.to_waveform()

        self.assertTupleEqual(iq.shape, (2*Settings().t_points,))
        self.assertTupleEqual(marker.shape, (Settings().t_points,))

    def test_to_waveform_dtype(self):
        self.iq_file = IQFile(self.filename_read, mode='r')
        iq, header, marker = self.iq_file.to_waveform()

        self.assertEqual(iq.dtype, np.dtype(">i2"))
        self.assertEqual(marker.dtype, np.dtype(">i1"))

    def test_from_txt(self):
        self.iq_file = IQFile.from_txt(self.filename_write, self.i_filename_read, self.q_filename_read, self.config_filename_read)
        self.assertTupleEqual((Settings().t_points,), self.iq_file.iq.shape)
        self.assertGreater(len(self.iq_file.header), 0)
        self.assertTupleEqual((Settings().t_points,), self.iq_file.marker.shape)

    def test_to_txt(self):
        self.iq_file = IQFile(self.filename_read, mode='r')
        self.iq_file.to_txt(self.i_filename_write, self.q_filename_write, self.config_filename_write)
        self.assertTrue(True)

    def test_tostring(self):
        self.iq_file = IQFile(self.filename_read, mode='r')
        self.assertTrue(self.iq_file.tostring().startswith(self.iq_string))

    def tearDown(self):
        if self.iq_file is not None:
            self.iq_file.close()


class Test_DatagroupBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Settings().num_harmonics = 2
        Settings().t_stop = 3e-6
        Settings().t_step = 1e-6

        cls.custom_sweep = np.array([1, 3, 2, 4, 5])
        cls.filename = root + os.sep + "test.h5"

    def setUp(self):
        self.dg = None

    def test_create_datagroup(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        self.assertTrue(True)

    def test_add_dataset(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        self.dg.add("Default")
        self.assertTrue(hasattr(self.dg.root, "Default"))

    def test_add_dataset_twice(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        self.dg.add("Default")
        with self.assertRaises(tb.exceptions.NodeError):
            self.dg.add("Default")

    def test_get_dataset(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        ds1 = self.dg.add("Default")
        ds2 = self.dg.dataset("Default")
        self.assertIs(ds1, ds2)

    def test_rename_dataset(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        ds1 = self.dg.add("Default")
        self.dg.rename("Default", "Default2")
        self.assertIs(ds1, self.dg.root.Default2)

    def test_remove_dataset(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        ds1 = self.dg.add("Default")
        self.dg.remove("Default")
        self.assertFalse(ds1._v_isopen)

    def tearDown(self):
        if self.dg is not None:
            self.dg.close()


class Test_DatasetBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Settings().num_harmonics = 2
        Settings().t_stop = 3e-6
        Settings().t_step = 1e-6

        cls.custom_sweep = np.array([1, 3, 2, 4, 5])
        cls.filename = root + os.sep + "test.h5"

    def setUp(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        self.ds = self.dg.add("Default")

    def test_add_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds))
        self.assertTrue(hasattr(self.ds, "Untitled"))

    def test_add_equation_twice(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds))
        equation_model2 = DatasetEquationModel(self.ds)
        self.ds.add(equation_model2.name, equation_model2.eval(self.ds))
        self.assertTrue(hasattr(self.ds, "Untitled"))
        self.assertTrue(hasattr(self.ds, "Untitled1"))

    def test_get_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        eq1 = self.ds.add(equation_model.name, equation_model.eval(self.ds))
        eq2 = self.ds.equation("Untitled")
        self.assertIs(eq1, eq2)

    def test_rename_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        eq1 = self.ds.add(equation_model.name, equation_model.eval(self.ds))
        self.ds.rename("Untitled", "Titled")
        self.assertIs(eq1, self.ds.Titled)

    def test_remove_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        eq1 = self.ds.add(equation_model.name, equation_model.eval(self.ds))
        self.ds.remove("Untitled")
        self.assertFalse(eq1._v_isopen)

    def tearDown(self):
        if self.dg is not None:
            self.dg.close()


class Test_DatasetAdvanced(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Settings().num_harmonics = 2
        Settings().t_stop = 3e-6
        Settings().t_step = 1e-6

        cls.custom_sweep = np.array([1, 3, 2, 4, 5])
        cls.filename = root + os.sep + "test.h5"

    def setUp(self):
        self.dg = DatagroupModel(self.filename, mode='w')
        self.ds = self.dg.add("Default")

    def test_add_signal_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".v_1 + .i_1"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    def test_add_bad_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        with self.assertRaises(AttributeError):
            self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".i_1 + .q1"))

    def test_add_mixed_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".v_1 + 1"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    @unittest.skip
    def test_add_equation_of_equation(self):
        #todo: convert all carrays in dataset to signalarray
        equation_model = DatasetEquationModel(self.ds, name="A")
        eq1 = self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn="1"))
        equation_model2 = DatasetEquationModel(self.ds)
        eq2 = self.ds.add(equation_model2.name, equation_model2.eval(self.ds, eqn=".v_1 + .A"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    def test_index_equaton(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".v_1[0, 0]"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    def test_subset_equation2(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".v_1[...]"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    def test_subset_equation(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".v_1[0, :]"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    def test_add_subset_equations(self):
        equation_model = DatasetEquationModel(self.ds)
        self.ds.add(equation_model.name, equation_model.eval(self.ds, eqn=".v_1[0, :] + .i_1[0, :]"))
        self.assertIsInstance(self.ds.Untitled[...], th.Tensor)

    def tearDown(self):
        if self.dg is not None:
            self.dg.close()


if __name__ == '__main__':
    unittest.main()
