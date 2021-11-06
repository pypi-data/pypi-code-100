import unittest
import os

import numpy as np
from numpy import testing as nptest

from sknrf.settings import Settings
from sknrf.app.dataviewer.model.mdif import MDIF, MDIFGroup, MDIFBlock
from sknrf.app.dataviewer.model.dataset import DatagroupModel

__author__ = 'dtbespal'

root = os.sep.join((Settings().data_root, "testdata", "mdif"))


def mdif_equal(test, mdif1, mdif2):
    test.assertEqual(mdif1.name, mdif2.name)
    for group1, group2 in zip(mdif1.dataBlocks, mdif2.dataBlocks):
        test.assertEqual(group1.name, group2.name)
        test.assertEqual(group1.type, group2.type)
        test.assertEqual(group1.sweeps, group2.sweeps)
        test.assertEqual(group1.sweepTypes, group2.sweepTypes)
        test.assertEqual(group1.independent, group2.independent)
        test.assertEqual(group1.independentType, group2.independentType)
        test.assertEqual(group1.attributes, group2.attributes)
        test.assertEqual(group1.attributesTypes, group2.attributesTypes)
        test.assertEqual(group1.dependents, group2.dependents)
        test.assertEqual(group1.dependentsTypes, group2.dependentsTypes)
        for block1, block2 in zip(group1.data, group2.data):
            test.assertEqual(len(block1.sweep), len(block2.sweep))
            test.assertEqual(block1.independent.shape, block2.independent.shape)
            test.assertEqual(len(block1.attributes), len(block2.attributes))
            test.assertEqual(block1.dependents.shape, block2.dependents.shape)


class TestMDIFValues(unittest.TestCase):

    def test_int(self):
        string_num = ['v1(0)', ' = ', '17']
        string_text = ['v1(int)', ' = ', '17']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'v1')
        self.assertIsInstance(value, np.int32)
        self.assertEqual(value, 17)

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'v1')
        self.assertIsInstance(value, np.int32)
        self.assertEqual(value, 17)

    def test_real(self):
        string_num = ['v1(1)', ' = ', '17.1']
        string_text = ['v1(real)', ' = ', '17.1']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'v1')
        self.assertIsInstance(value, float)
        self.assertAlmostEqual(value, 17.1)

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'v1')
        self.assertIsInstance(value, float)
        self.assertAlmostEqual(value, 17.1)

    def test_string(self):
        string_num = ['att3(2)', ' = ', '"Hello, World"']
        string_text = ['att3(string)', ' = ', '"Hello, World"']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, str)
        self.assertEqual(value, '"Hello, World"')

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, str)
        self.assertEqual(value, '"Hello, World"')

    def test_complex(self):
        pass

    def test_boolean(self):
        string_num = ['att3(4)', ' = ', '0']
        string_text = ['att3(boolean)', ' = ', '1']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, bool)
        self.assertEqual(value, False)

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, bool)
        self.assertEqual(value, True)

    def test_binary(self):
        string_num = ['att3(5)', ' = ', '0b0010001']
        string_text = ['att3(binary)', ' = ', '0b0010001']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0b0010001)

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0b0010001)

    def test_octal(self):
        string_num = ['att3(6)', ' = ', '0o021']
        string_text = ['att3(octal)', ' = ', '0o021']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0o021)

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0o021)

    def test_hexadecimal(self):
        string_num = ['att3(7)', ' = ', '0x11']
        string_text = ['att3(hexadecimal)', ' = ', '0x11']

        name, type = MDIF._get_name_type(string_num[0])
        value = MDIF._get_value(string_num[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0x11)

        name, type = MDIF._get_name_type(string_text[0])
        value = MDIF._get_value(string_text[2], type)
        self.assertEqual(name, 'att3')
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0x11)

    def test_byte(self):
        pass


class TestMDIFRead(unittest.TestCase):

    def test_01_comment(self, read_filename="comment.mdf"):
        self.mdif_ref = MDIF(read_filename)
        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        mdif_equal(self, self.mdif_read, self.mdif_ref)

    def test_02_sweep(self, read_filename="sweep.mdf"):
        self.test_01_comment(read_filename)
        self.mdif_ref.dataBlocks.append(MDIFGroup('DSCR()'))
        self.mdif_ref.dataBlocks[0].sweeps = ["v1", "v2", "v3"]
        self.mdif_ref.dataBlocks[0].sweepTypes = ["0", "1", "2"]
        self.mdif_ref.dataBlocks[0].independent = "index"
        self.mdif_ref.dataBlocks[0].independentType = "int"
        self.mdif_ref.dataBlocks[0].data.append(MDIFBlock())
        self.mdif_ref.dataBlocks[0].data[0].sweep = [1, 2.2, "Hello World"]
        self.mdif_ref.dataBlocks[0].data[0].independent = np.array([], dtype=np.complex)

        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        mdif_equal(self, self.mdif_read, self.mdif_ref)

    def test_03_attribute(self, read_filename='attribute.mdf'):
        self.test_02_sweep()
        self.mdif_ref.name = read_filename
        self.mdif_ref.dataBlocks[0].attributes = ["v1", "v2", "v3"]
        self.mdif_ref.dataBlocks[0].attributesTypes = ["0", "1", "2"]
        self.mdif_ref.dataBlocks[0].data[0].independent = np.array([], dtype=np.complex)
        self.mdif_ref.dataBlocks[0].data[0].attributes = [1, 2.2, "Hello World"]

        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        mdif_equal(self, self.mdif_read, self.mdif_ref)

    def test_04_dependent(self, read_fileanme='dependent.mdf'):
        self.test_03_attribute()

        self.mdif_ref.name = read_fileanme
        self.mdif_ref.dataBlocks[0].name = 'blk1'
        self.mdif_ref.dataBlocks[0].independent = "v1"
        self.mdif_ref.dataBlocks[0].independentType = "real"
        self.mdif_ref.dataBlocks[0].dependents = ["v2", "v3"]
        self.mdif_ref.dataBlocks[0].dependentsTypes = ["complex", "complex"]
        self.mdif_ref.dataBlocks[0].data[0].independent = np.array([1e9, 2e9], dtype=np.float)
        self.mdif_ref.dataBlocks[0].data[0].dependents = np.array([[2.2222 + 2.2222j, 3.3333 + 3.3333j],
                                                                   [4.4444 + 4.4444j, 6.6666 + 6.6666j]],
                                                                  dtype=np.complex)

        self.mdif_read = MDIF.read(root + os.sep + read_fileanme)
        mdif_equal(self, self.mdif_read, self.mdif_ref)

    def test_05_group(self, read_filename='group.mdf'):
        self.test_04_dependent()
        self.mdif_ref.name = read_filename
        self.mdif_ref.dataBlocks[0].data.append(MDIFBlock())
        self.mdif_ref.dataBlocks[0].data[1].sweep = [2, 4.4, "Hello Again"]
        self.mdif_ref.dataBlocks[0].data[1].independent = np.array([8, 9], dtype=np.complex)
        self.mdif_ref.dataBlocks[0].data[1].attributes = [12, 4.4, "Hello World"]
        self.mdif_ref.dataBlocks[0].data[1].dependents = np.array([[8.8888 + 8.8888j, 10.0000 + 10.0000j],
                                                                  [9.9999 + 9.9999j, 12.0000 + 12.0000j]],
                                                                  dtype=np.complex)

        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        mdif_equal(self, self.mdif_read, self.mdif_ref)


class TestMDIFRead2(unittest.TestCase):

    @unittest.skip  # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_s2d1(self, read_filename="S2D1.s2d"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)

    @unittest.skip # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_s2d2(self, read_filename="S2D2.s2d"):
        # Removed the IMTDATA from the original file
        self.mdif_read = MDIF.read(root + os.sep + read_filename)

    @unittest.skip  # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_p2d1(self, read_filename="P2D1.p2d"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)

    @unittest.skip # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_tim(self, read_filename="TIM1.tim"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)

    def test_dscr(self, read_filename="DSCR1.dscr"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)


class TestMDIFStrings(unittest.TestCase):

    def test_int(self):
        values_num = ('v1', '0', 17)
        values_text = ('v1', 'int', 17)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'v1(0) =              17')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'v1(int) =              17')

    def test_real(self):
        values_num = ('v1', '1', 17.1)
        values_text = ('v1', 'real', 17.1)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'v1(1) =     17.10000000')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'v1(real) =     17.10000000')

    def test_string(self):
        values_num = ('att3', '2', '"Hello, World"')
        values_text = ('att3', 'string', '"Hello, World"')

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'att3(2) = "Hello, World"')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'att3(string) = "Hello, World"')

    def test_complex(self):
        values_num = ('att3', '3', 1 + 2j)
        values_text = ('att3', 'complex', 1 + 2j)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'att3(3) =      1.00000000     2.00000000')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'att3(complex) =      1.00000000     2.00000000')

    def test_boolean(self):
        values_num = ('att3', '4', False)
        values_text = ('att3', 'boolean', True)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'att3(4) = 0')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'att3(boolean) = 1')

    def test_binary(self):
        values_num = ('att3', '5', 17)
        values_text = ('att3', 'binary', 17)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'att3(5) = 0b10001')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'att3(binary) = 0b10001')

    def test_octal(self):
        values_num = ('att3', '6', 17)
        values_text = ('att3', 'octal', 17)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'att3(6) = 0o21')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'att3(octal) = 0o21')

    def test_hexadecimal(self):
        values_num = ('att3', '7', 17)
        values_text = ('att3', 'hexadecimal', 17)

        string =  MDIF._get_string(values_num[2], values_num[1])
        string_out = '%s(%s) = %s' % (values_num[0], values_num[1], string)
        self.assertEqual(string_out, 'att3(7) = 0x11')

        string =  MDIF._get_string(values_text[2], values_text[1])
        string_out = '%s(%s) = %s' % (values_text[0], values_text[1], string)
        self.assertEqual(string_out, 'att3(hexadecimal) = 0x11')

    def test_byte(self):
        pass


class TestMDIFWrite(unittest.TestCase):

    @unittest.skip  # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_s2d1(self, read_filename="S2D1.s2d", write_filename="S2D1_write.s2d"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        self.mdif_read.write(root + os.sep + write_filename)

    @unittest.skip  # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_s2d2(self, read_filename="S2D2.s2d", write_filename="S2D2_write.s2d"):
        # Removed the IMTDATA from the original file
        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        self.mdif_read.write(root + os.sep + write_filename)

    @unittest.skip  # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_p2d1(self, read_filename="P2D1.p2d", write_filename="P2D1_write.p2d"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        self.mdif_read.write(root + os.sep + write_filename)

    @unittest.skip  # MDIF Parser does not support complex attributes #AC( GHZ S RI R 50.0 FC 1 15 )
    def test_tim(self, read_filename="TIM1.tim", write_filename="TIM1_write.tim"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        self.mdif_read.write(root + os.sep + write_filename)

    def test_dscr(self, read_filename="DSCR1.dscr", write_filename="DSCR1_write.dscr"):
        self.mdif_read = MDIF.read(root + os.sep + read_filename)
        self.mdif_read.write(root + os.sep + write_filename)


class Test01MDIFReadDatagroup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Settings().datagroup = "TestMDIF"

    def test_single_dataset(self, read_filename="test_single.mdf"):
        datagroup = DatagroupModel(mode="a")
        filename = root + os.sep + read_filename
        MDIF.read_dataset(datagroup, filename, group_index=0)
        datagroup.close()

    def test_sweep_dataset(self, read_filename="test_sweep.mdf"):
        datagroup = DatagroupModel(mode="a")
        filename = root + os.sep + read_filename
        MDIF.read_dataset(datagroup, filename, group_index=0)
        datagroup.close()

    def test_datagroup(self, read_filename="test_datagroup.mdf"):
        filename = root + os.sep + read_filename
        datagroup = MDIF.read_datagroup(filename)
        datagroup.close()


class Test02MDIFWriteDatagroup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Settings().datagroup = "TestMDIF"

    def test_single_dataset(self, write_filename="test_single_write.mdf"):
        datagroup = DatagroupModel(mode="r")
        dataset = datagroup.dataset("test_single")
        MDIF.write_dataset(dataset, root + os.sep + write_filename)

    def test_sweep_dataset(self, write_filename="test_sweep_write.mdf"):
        datagroup = DatagroupModel(mode="r")
        dataset = datagroup.dataset("test_sweep")
        MDIF.write_dataset(dataset, root + os.sep + write_filename)

    def test_datagroup(self, write_filename="test_datagroup_write.mdf"):
        datagroup = DatagroupModel(mode="r")
        MDIF.write_datagroup(datagroup, root + os.sep + write_filename)
