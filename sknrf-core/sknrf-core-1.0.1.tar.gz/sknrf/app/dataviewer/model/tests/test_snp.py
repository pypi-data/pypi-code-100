import unittest
import os

from sknrf.settings import Settings
from sknrf.app.dataviewer.model.snp import SNP
from sknrf.app.dataviewer.model.dataset import DatagroupModel

__author__ = 'dtbespal'

root = os.sep.join((Settings().data_root, "testdata", "snp"))


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


class TestSNPRead(unittest.TestCase):

    def test_s1p_KHZ_S_RI_R_50(self, read_filename="S1P.s1p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)

    def test_s2p_GHZ_S_RI_R_50(self, read_filename="S2P.s2p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)

    def test_s3p_GHZ_S_DB_R_50(self, read_filename="S3P.s3p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)

    def test_s4p_GHZ_S_MA_R_50(self, read_filename="S4P.s4p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)

    def test_y3p_GHZ_Y_MA_R_1(self, read_filename="Y3P.s3p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)


class TestSNPWrite(unittest.TestCase):

    def test_s1p_KHZ_S_RI_R_50(self, read_filename="S1P.s1p", write_filename="S1P_write.s1p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)
        self.snp_read.write(root + os.sep + write_filename)

    def test_s2p_GHZ_S_RI_R_50(self, read_filename="S2P.s2p", write_filename="S2P_write.s2p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)
        self.snp_read.write(root + os.sep + write_filename)

    def test_s3p_GHZ_S_DB_R_50(self, read_filename="S3P.s3p", write_filename="S3P_write.s3p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)
        self.snp_read.write(root + os.sep + write_filename)

    def test_s4p_GHZ_S_MA_R_50(self, read_filename="S4P.s4p", write_filename="S4P_write.s4p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)
        self.snp_read.write(root + os.sep + write_filename)

    def test_y3p_GHZ_Y_MA_R_1(self, read_filename="Y3P.s3p", write_filename="Y3P_write.s3p"):
        self.snp_read = SNP.read(root + os.sep + read_filename)
        self.snp_read.write(root + os.sep + write_filename)


class TestSNPReadNetwork(unittest.TestCase):

    def test_read_network(self, read_filename="S2P.s2p"):
        network = SNP.read_network(root + os.sep + read_filename)


class TestSNPWriteNetwork(unittest.TestCase):

    def test_write_network(self, read_filename="S2P.s2p", write_network_filename="S2P_write_network.s2p"):
        network = SNP.read_network(root + os.sep + read_filename)
        SNP.write_network(network, root + os.sep + write_network_filename)


class TestSNPReadDatagroup(unittest.TestCase):

    @unittest.skip
    def test_single_dataset(self, read_filename="S2P.s2p"):
        datagroup = DatagroupModel(mode="a")
        dataset_name = "testSNPWrite__test_single_dataset"
        dataset = SNP.read_dataset(datagroup, root + os.sep + read_filename, Settings().num_ports, group_index=0)

    @unittest.skip
    def test_datagroup(self, read_filename="S2P.s2p"):
        datagroup = SNP.read_datagroup(root + os.sep + read_filename, Settings().num_ports)


class TestSNPWriteDatagroup(unittest.TestCase):

    @unittest.skip
    def test_single_dataset(self, write_filename="S2P_write_dataset.s2p"):
        # Create the Dataset
        dataset_name = "testSNPWrite__test_single_dataset"
        datagroup = DatagroupModel(mode="a")
        if datagroup.has_dataset(dataset_name):
            datagroup.remove(dataset_name)
        dataset = datagroup.add(dataset_name)
        SNP.write_dataset(dataset, root + os.sep + write_filename)

    @unittest.skip
    def test_datagroup(self, write_filename="S2P_write_datagroup.s2p"):
        # Create the Datagroup
        datagroup = DatagroupModel(mode="a")
        dataset_name = "testSNPWrite__test_datagroup1"
        if datagroup.has_dataset(dataset_name):
            datagroup.remove(dataset_name)
        datagroup.add(dataset_name)
        dataset_name = "testSNPWrite__test_datagroup2"
        if datagroup.has_dataset(dataset_name):
            datagroup.remove(dataset_name)
        datagroup.add(dataset_name)
        SNP.write_datagroup(datagroup, root + os.sep + write_filename)

