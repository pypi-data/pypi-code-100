"""
===============================================
SNP File (:mod:`sknrf.model.dataviewer.snp`)
===============================================

This module converts between the Touchstone text format, the SNP object format, Scikit-rf network, and the sknrf datagroup.

Touchstone Text Format
----------------------

`Touchstone Specification`_

Note
----
The Touchstone Specification is supported with the following exceptions:
    * Depedent parameters are assumed to be complex numbers.

See Also
--------
sknrf.model.dataviewer.mdif.MDIF, sknrf.model.dataviewer.dataset.DatagroupModel, sknrf.model.dataviewer.dataset.DatasetModel


.. _Touchstone Specification:
    http://cp.literature.agilent.com/litweb/pdf/ads2004a/cktsim/ck04a8.html

"""
import re
import os
import logging

import numpy as np
import skrf as rf

from sknrf.app.dataviewer.model.dataset import DatagroupModel
from sknrf.app.dataviewer.model.mdif import MDIF, MDIFGroup, MDIFBlock, _complex2str
from sknrf.utilities.numeric import Scale, lin_deg2re_im, re_im2lin_deg,log_deg2re_im, re_im2log_deg,re_im2re_im

logger = logging.getLogger(__name__)


class SNPBlock(MDIFBlock):
    pass


class SNPGroup(MDIFGroup):
    pass


class SNP(MDIF):
    """SNP Object

    The SNP object contains a SNPGroup for each measurement. It allows read/write access to the SNP file format.

    Parameters
    ----------
    name : str
        Name of the SNP file.
    date : str
        Creation date/time of the SNP File
    dataBlocks : list of :class:`~sknrf.model.dataviewer.mdif.SNPGroup` objects

    """

    _freq_scale_map = {"HZ":  10**0,
                       "KHZ": 10**3,
                       "MHZ": 10**6,
                       "GHZ": 10**9}
    _format_map = {"MA": lin_deg2re_im,
                         "DB": log_deg2re_im,
                         "RI": re_im2re_im}
    _format_inv_map = {"MA": re_im2lin_deg,
                         "DB": re_im2log_deg,
                         "RI": re_im2re_im}

    def __init__(self, name="", date="", dataBlocks=None):
        super(SNP, self).__init__(name=name, date=date, dataBlocks=dataBlocks)

    @staticmethod
    def read(filename):
        """Reads a Touchstone text file into the SNP object.

        Parameters
        ----------
        filename : str
            SNP filename.

        Returns
        -------
        SNP
            A new SNP object.

        """

        # Todo support multiple sections
        root, group = SNP(filename), SNPGroup("")
        num_ports = int(os.path.splitext(filename)[1][2])
        pattern = re.compile(r'("[^"]*"|\S+)')
        block_name, inside_block = "Untitled", False
        sweep_names, sweep_types, sweep_values = [], [], []
        attribute_names, attribute_types, attribute_values = [None]*4, [None]*4, [None]*4
        dependent_names, dependent_types, dependent_values = [], [], []
        line_index = 0

        dependent_names.append("freq")
        dependent_types.append("real")
        for rcvr_index in range(num_ports):
            for src_index in range(num_ports):
                dependent_names.append("%s%d%d" % (attribute_values[1], rcvr_index, src_index))
                dependent_types.append("complex")

        # Parse the file
        with open(filename) as f:
            for line in f:
                try:
                    line = line.strip()
                    line_index += 1
                    if line and not line.startswith(("!", "REM")):
                        # Tokenize the line
                        tokens = pattern.findall(line)
                        if tokens[0].startswith('#'):
                            if len(tokens[0]) > 1:
                                tokens[0] = tokens[0][1::]
                            else:
                                tokens = tokens[1::]
                            if inside_block:
                                raise IOError("Unexpected attributes on line:%d %s" % (line_index, line))
                            inside_block = True
                            tokens = [token.upper() for token in tokens]
                            if tokens[0] not in root._freq_scale_map:
                                raise ValueError("Unexpected scale %s on line:%d %s" % (tokens[0], line_index, line))
                            attribute_names[0], attribute_types[0], attribute_values[0] = "scale", "string", tokens[0]
                            if tokens[1] not in ["S", "Y", "Z", "G", "H"]:
                                raise ValueError("Unexpected parameter %s on line:%d %s" % (tokens[1], line_index, line))
                            attribute_names[1], attribute_types[1], attribute_values[1] = "parameter", "string", tokens[1]
                            if tokens[2] not in root._format_map:
                                raise ValueError("Unexpected format %s on line:%d %s" % (tokens[2], line_index, line))
                            attribute_names[2], attribute_types[2], attribute_values[2] = "parameter", "string", tokens[2]
                            attribute_names[3], attribute_types[3], attribute_values[3] = "impedance", "real",\
                                                                                          np.float64(tokens[4])
                        else:
                            if not inside_block:
                                raise IOError("Unknown Command on line:%d %s" % (line_index, line))
                            if not dependent_values or len(dependent_values[-1]) == len(dependent_names)*2 - 1:
                                dependent_values.append([])
                            dependent_values[-1] += tokens
                except Exception as e:
                    message = str(e) + " Error reading line:%d %s" % (line_index, line)
                    logger.error(message, exc_info=True)
                    raise type(e)(message)

            if not inside_block:
                raise ValueError("No S-Parameter Data found in File")
            block = SNPBlock(sweep=sweep_values, attributes=attribute_values)
            scale = root._freq_scale_map[attribute_values[0]]
            format_ = root._format_map[attribute_values[2]]
            dependent_array = np.asarray(dependent_values, dtype='<S12')
            independent_name = dependent_names[0]
            independent_type = dependent_types[0]
            block.independent = dependent_array[:, 0].astype(np.float64)*scale
            dependent_names = dependent_names[1:]
            dependent_types = dependent_types[1:]
            block.dependents = dependent_array[:, 1:].astype(np.float64)
            block.dependents.dtype = np.complex
            block.dependents = format_(block.dependents)
            if group.name != block_name:
                if group.name:
                    root.dataBlocks.append(group)
                group = MDIFGroup(block_name,
                                  sweeps=sweep_names, sweep_types=sweep_types,
                                  attributes=attribute_names, attribute_types=attribute_types,
                                  independent=independent_name, independent_type=independent_type,
                                  dependents=dependent_names, dependent_types=dependent_types,
                                  data=[])
            group.data.append(block)
        root.dataBlocks.append(group)
        return root

    @staticmethod
    def read_network(filename):
        """Reads a Touchstone text file into the scikit-rf network object.

        Parameters
        ----------
        filename : str
            SNP filename.

        Returns
        -------
        rf.Network
            A new Scikit-rf network object.

        """
        root = SNP.read(filename)
        group = root.dataBlocks[0]
        block = group.data[0]
        num_ports = int(os.path.splitext(filename)[1][2])
        name = os.path.splitext(os.path.basename(filename))[0]
        network = rf.Network(name=name, frequency=block.independent, s=block.dependents.reshape(-1, num_ports, num_ports))
        return network

    @staticmethod
    def read_dataset(datagroup, filename, num_ports, group_index=0):
        root = SNP.read(filename)
        return root._import_dataset(datagroup, filename, num_ports, group_index=group_index)

    @staticmethod
    def read_datagroup(filename, num_ports):
        root = SNP.read(filename)
        datagroup = DatagroupModel(mode="a")
        for group_index in range(len(root.dataBlocks)):
            root._import_dataset(datagroup, filename, num_ports, group_index=group_index, use_group_name=True)
        return datagroup

    def write(self, filename):
        """Writes a SNP object to an SNP text file.

        Parameters
        ----------
        filename : str
            SNP filename.

        """
        # Todo: Insert header comments
        with open(filename, mode="w") as f:
            for group in self.dataBlocks:
                for block in group.data:
                    # Block Attributes
                    scale = self._freq_scale_map[block.attributes[0]]
                    _format_inv = self._format_inv_map[block.attributes[2]]
                    f.write('# %s %s %s R %d\n' % tuple(block.attributes))
                    f.write("    ".join(['!'] +['%s']*len(group.dependents) + ['\n']) % tuple(group.dependents))
                    # Block Dependents
                    dependents = np.concatenate((block.independent[:, np.newaxis]/scale,
                                                 _format_inv(block.dependents)), axis=1)
                    dependentsTypes = [group.independentType] + ["3"]*len(group.dependentsTypes)

                    for row in range(dependents.shape[0]):
                        f.write(self._get_string(dependents[row, 0].real, dependentsTypes[0])
                                + "".join(map(_complex2str, dependents[row, 1:])) + "\n")

    @staticmethod
    def write_network(network, filename):
        """Writes a Scikit-rf network to an SNP text file.

        Parameters
        ----------
        network : rf.network
            Scikit-rf network
        filename : str
            SNP filename.

        """
        block_name = "SParameters"
        root, group, block = SNP(), SNPGroup(block_name), SNPBlock()
        sweep_names, sweep_types, sweep_values = [], [], []
        dependent_names, dependent_types, dependent_values = [], [], []

        # Block Attributes
        attribute_names = ["frequency_unit", "parameter_type", "format", "impedance"]
        attribute_types = ["string", "string", "string", "real"]
        attribute_values = [network.frequency.unit.upper(), "S", "MA", 50]

        # Block Independent
        independent_name = "f"
        independent_type = "real"
        independent_values = network.f

        # Block Dependent
        num_ports = network.nports
        for rcvr_index in range(1, num_ports + 1):
            for src_index in range(1, num_ports + 1):
                dependent_names.append(attribute_values[1] + str(rcvr_index) + str(src_index))
                dependent_types.append("complex")
        dependent_values = np.asarray(network.s, dtype=np.complex).reshape(network.f.shape[0], -1)

        group = SNPGroup(name=block_name, sweeps=sweep_names, sweep_types=sweep_types,
                          independent=independent_name, independent_type=independent_type,
                          attributes=attribute_names, attribute_types=attribute_types,
                          dependents=dependent_names, dependent_types=dependent_types,
                          data=[])
        block = SNPBlock(sweep=sweep_values, attributes=attribute_values,
                         independent=independent_values, dependents=dependent_values)
        group.data.append(block)
        root.dataBlocks.append(group)
        root.write(filename)

    @staticmethod
    def _get_name_type(string):
        """Parse the name(type) string

        Parameters
        ----------
        string : str
            string in the form of: name(type)

        """
        name = string[0:string.find("(")]
        type = string[string.find("(")+1:string.find(")")]
        return name, type
