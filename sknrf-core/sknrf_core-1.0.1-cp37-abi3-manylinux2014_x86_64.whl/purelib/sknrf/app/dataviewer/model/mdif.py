"""
===============================================
MDIF File (:mod:`sknrf.model.dataviewer.mdif`)
===============================================

This module converts between the MDIF text format, the MDIF object format, and the sknrf datagroup.

MDIF Text Format
----------------

`MDIF Specification`_

Note
----
The MDIF Specification is supported with the following exceptions:
    * Depedent parameters are assumed to be complex numbers.
    * Dependent parameters cannot be sparse matricies
    * Dependent paramters cannot contain measurement units

See Also
--------
sknrf.model.dataviewer.dataset.DatagroupModel, sknrf.model.dataviewer.dataset.DatasetModel, sknrf.model.dataviewer.snp.SNP


.. _MDIF Specification:
    http://cp.literature.agilent.com/litweb/pdf/ads2004a/cktsim/ck0418.html

"""
import re
import os
import datetime
import time
import logging
from collections import OrderedDict

import numpy as np
import torch as th

from sknrf.app.dataviewer.model.dataset import DatagroupModel, DatasetModel
from sknrf.app.dataviewer.model.equation import SignalArray

spacing = 15
precision = 8
logger = logging.getLogger(__name__)


def _str2bool(string):
    return np.bool(np.int32(string))


def _str2bin(string):
    return int(string, 2)


def _str2oct(string):
    return int(string, 8)


def _str2hex(string):
    return int(string, 16)


def _int2str(value):
    return "%*d" % (spacing, value)


def _float2str(value):
    return "%*.*f" % (spacing, precision, value)


def _complex2str(value, format_="RI"):
    if format_ == "MA":
        return "%*.*f%*.*f" % (spacing, precision, np.abs(value), spacing, precision, np.angle(value) * 180 / np.pi)
    elif format_ == "DB":
        return "%*.*f%*.*f" % (
            spacing, precision, 20 * np.log10(np.abs(value)), spacing, precision, np.angle(value) * 180 / np.pi)
    elif format_ == "RI":
        return "%*.*f%*.*f" % (spacing, precision, value.real, spacing, precision, value.imag)
    else:
        raise AttributeError("Unsupported numeric format")


def _bool2str(value):
    return 1 if value else 0


class MDIFBlock(object):
    """MDIF Block Object

    The MDIF Block contains the measurement response for a given measurement sweep index.

    Parameters
    ----------
    sweep : list
        Values of the sweep parameters.
    attributes : list
        Values of the attributes parameters.
    independent : numpy ndarray
        Values of the independent parameter.
    dependents : numpy ndarray
        Values of the dependents parameters.
    """
    def __init__(self, sweep=None, attributes=None, independent=None, dependents=None):
        self.sweep = sweep if sweep else []
        self.attributes = attributes if attributes else []
        self.independent = independent if independent is not None else np.empty(0)
        self.dependents = dependents if dependents is not None else np.empty(0)


class MDIFGroup(object):
    """MDIF Group Object

    The MDIF Group contains a MDIFBlock for each measurement sweep index.

    Parameters
    ----------
    name : str
        Name of the MDIF file.
    type : str
        Name of the measurement type.
    sweeps : list of str
        Names of the sweep parameters.
    sweep_types : list of str
        Data types of the sweep parameters.
    attributes : list of str
        Names of the attribute parameters.
    attribute_types : list of str
        Data types of the attribute parameters.
    independent : str
        Names of the independent (inner) sweep parameter.
    independent_type : str
        Data type of the independent sweep parameter.
    dependents : list of str
        Names of the dependent parameters.
    dependent_types : list of str
        Data types of the dependent parameters.
    data : list of :class:`~sknrf.model.dataviewer.mdif.MDIFBlock` objects

    """
    def __init__(self, name, type_="",
                 sweeps=None, sweep_types=None,
                 attributes=None, attribute_types=None,
                 independent="", independent_type="",
                 dependents=None, dependent_types=None,
                 data=None):
        self.name, self.type = name, type_
        self.sweeps = sweeps if sweeps else []
        self.sweepTypes = sweep_types if sweep_types else []
        self.attributes = attributes if attributes else []
        self.attributesTypes = attribute_types if attribute_types else []
        self.independent = independent
        self.independentType = independent_type
        self.dependents = dependents if dependents else []
        self.dependentsTypes = dependent_types if dependent_types else []
        self.data = data if data else []


class MDIF(object):
    """MDIF Object

    The MDIF object contains a MDIFGroup for each measurement. It allows read/write access to the MDIF file format.

    Parameters
    ----------
    name : str
        Name of the MDIF file.
    date : str
        Creation date/time of the MDIF File
    dataBlocks : list of :class:`~sknrf.model.dataviewer.mdif.MDIFGroup` objects

    """

    def __init__(self, name, date="", dataBlocks=None):
        path, filename = os.path.split(name)
        creation_time = os.path.getctime(name) if path else time.time()
        self.name = filename
        self.date = date if date else datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        self.dataBlocks = dataBlocks if dataBlocks else []

    @staticmethod
    def read(filename):
        """Reads an MDIF text file into the MDIF object.

        Parameters
        ----------
        filename : str
            MDIF filename.

        Returns
        -------
        MDIF
            A new MDIF object.

        """
        # Todo Depedent Variables are assumed to be complex for faster reading
        # Todo Dependent Varaiables cannot be sparse matricies
        # Todo Parse Units
        root, group = MDIF(filename), MDIFGroup("")

        pattern = re.compile(r'("[^"]*"|\S+)')
        block_name, inside_block = "Untitled", False
        sweep_names, sweep_types, sweep_values = [], [], []
        attribute_names, attribute_types, attribute_values = [], [], []
        dependent_names, dependent_types, dependent_values = [], [], []
        line_index = 0

        # Parse the file
        with open(filename) as f:
            for line in f:
                try:
                    line = line.strip()
                    line_index += 1
                    if line and not line.startswith(("!", "REM")):
                        # Tokenize the line
                        tokens = pattern.findall(line)
                        if tokens[0].startswith(("VAR", "ValueVAR")):
                            if inside_block:
                                raise IOError("Unexpected sweep variable")
                            name, type_ = MDIF._get_name_type(tokens[1])
                            sweep_names.append(name)
                            sweep_types.append(type_)
                            sweep_values.append(MDIF._get_value(tokens[3], type_))
                        elif tokens[0].startswith("BEGIN"):
                            if inside_block:
                                raise IOError("Unexpected BEGIN")
                            inside_block = True
                            block_name = tokens[1]
                        elif tokens[0].startswith('#'):
                            if len(tokens[0]) > 1:
                                tokens[0] = tokens[0][1::]
                            else:
                                tokens = tokens[1::]
                            if not inside_block:
                                raise IOError("Unexpected attributes")
                            name, type_ = MDIF._get_name_type(tokens[0])
                            attribute_names.append(name)
                            attribute_types.append(type_)
                            attribute_values.append(MDIF._get_value(tokens[2], type_))
                        elif tokens[0].startswith('%'):
                            if len(tokens[0]) > 1:
                                tokens[0] = tokens[0][1::]
                            else:
                                tokens = tokens[1::]
                            if not inside_block:
                                raise IOError("Unexpected dependents")
                            for index in range(len(tokens)):
                                name, type_ = MDIF._get_name_type(tokens[index])
                                dependent_names.append(name)
                                dependent_types.append(type_)
                        elif tokens[0].startswith("END"):
                            inside_block = False
                            block = MDIFBlock(sweep=sweep_values, attributes=attribute_values)
                            dependent_array = np.asarray(dependent_values, dtype='<S12')
                            if block_name.startswith("DSCR"):  # Implicit index independent variable
                                independent_name = "index"
                                independent_type = "int"
                                block.independent = np.arange(1, dependent_array.shape[0]+1)
                                if dependent_names:
                                    dependent_names = dependent_names[1:]
                                    dependent_types = dependent_types[1:]
                                    block.dependents = dependent_array[:, 1:].astype(np.float64)
                                    block.dependents.dtype = np.complex
                            else:  # Explicit independent variable is the first dependent variable
                                independent_name = dependent_names[0]
                                independent_type = dependent_types[0]
                                block.independent = dependent_array[:, 0].astype(np.float64)
                                dependent_names = dependent_names[1:]
                                dependent_types = dependent_types[1:]
                                block.dependents = dependent_array[:, 1:].astype(np.float64)
                                block.dependents.dtype = np.complex
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
                            block_name, inside_block = "", False
                            sweep_names, sweep_types, sweep_values = [], [], []
                            attribute_names, attribute_types, attribute_values = [], [], []
                            dependent_names, dependent_types, dependent_values = [], [], []
                        else:
                            if not inside_block:
                                raise IOError("Unknown Command")
                            if not dependent_values or len(dependent_values[-1]) == len(dependent_names)*2 - 1:
                                dependent_values.append([])
                            dependent_values[-1] += tokens
                except Exception as e:
                    message = str(e) + " Error reading line:%d %s" % (line_index, line)
                    logger.error(message, exc_info=True)
                    raise type(e)(message)
        root.dataBlocks.append(group)
        return root

    def _import_dataset(self, dg, filename, group_index=0, use_group_name=False):

        group = self.dataBlocks[group_index]

        # Indep_map
        sweep_map = OrderedDict()
        sweep_names = group.sweeps
        sweep_values = [[sweep] for sweep in group.data[0].sweep]
        block_index = 1
        sweep_index = len(sweep_names) - 1
        step = 1
        while block_index < len(group.data):
            if group.data[block_index].sweep[sweep_index] == sweep_values[sweep_index][0]:
                step *= len(sweep_values[sweep_index])
                sweep_index -= 1
            sweep_values[sweep_index].append(group.data[block_index].sweep[sweep_index])
            block_index += step
        sweep_names.append(group.independent)
        sweep_values.append(group.data[0].independent)
        for sweep_index, (sweep_name, sweep_value) in enumerate(zip(reversed(sweep_names), reversed(sweep_values))):
            sweep_value = th.as_tensor(np.asarray(sweep_value).astype(np.float), dtype=th.double)
            sweep_shape = list(sweep_value.shape)
            while len(sweep_shape) < sweep_index + 1:
                sweep_shape.insert(1, 1)
            while len(sweep_shape) < len(sweep_values):
                sweep_shape.insert(0, 1)
            sweep_value = sweep_value.reshape(sweep_shape)
            sweep_map[sweep_name] = th.as_tensor(sweep_value)

        # Dataset Equations
        ds_name = group.name if use_group_name else os.path.splitext(os.path.split(filename)[1])[0]
        if dg.has_dataset(ds_name):
            dg.remove(ds_name)
        ds = dg.add(ds_name, ports=(), duts=(), mipis=(), videos=(), sweep_map=sweep_map)
        for dependent_name in group.dependents:
            if not ds.has_equation(dependent_name):
                ds.add(dependent_name, th.zeros(ds.shape))
        step = sweep_map["f"].shape[-1]
        di = ds.__iter__(step, sweep_enabled=False)
        for iteration, block in zip(di, group.data):
            array_index = di.array_index
            for dep_index, dependent_name in zip(range(block.dependents.shape[1]), group.dependents):
                getattr(ds, dependent_name)[array_index] = block.dependents[:, dep_index]
        return ds

    @staticmethod
    def read_dataset(datagroup, filename, group_index=0):
        """Reads an MDIF text file dataBlock into a dataset.

        Parameters
        ----------
        datagroup : DatagroupModel
            Parent datagroup where the resulting dataset is stored.
        filename : str
            MDIF filename.
        group_index : int
            MDIF dataBlock index
        use_group_name : bool
            If True (default), use the MDIF dataBlock name as the dataset name.
            If False, use the MDIF filename as the dataset name.

        Returns
        -------
        DatasetModel
            A new dataset.

        """
        root = MDIF.read(filename)
        return root._import_dataset(datagroup, filename, group_index=group_index)

    @staticmethod
    def read_datagroup(filename, class_=None):
        """Reads an MDIF text file into an existing datagroup.

        Parameters
        ----------
        filename : str
            MDIF filename.

        Returns
        -------
        DatagroupModel
            A new datagroup.

        """
        class_ = MDIF if class_ is None else class_
        root = class_.read(filename)
        datagroup = DatagroupModel(mode="a")
        for group_index in range(len(root.dataBlocks)):
            root._import_dataset(datagroup, filename, group_index=group_index, use_group_name=True)
        return datagroup

    def write(self, filename):
        """Writes a MDIF object to an MDIF text file.

        Parameters
        ----------
        filename : str
            MDIF filename.

        """

        #Todo: Insert header comments
        with open(filename, mode="w") as f:
            for group in self.dataBlocks:
                for block in group.data:
                    for name, type_, value in zip(group.sweeps, group.sweepTypes, block.sweep):
                        string = self._get_string(value, type_)
                        f.write('VAR %s(%s) = %s\n'% (name, type_, string))
                    f.write('BEGIN %s\n' % group.name)
                    for name, type_, value in zip(group.attributes, group.attributesTypes, block.attributes):
                        string = self._get_string(value, type_)
                        f.write('# %s(%s) = %s\n'% (name, type_, string))
                    if group.name[0:4] == 'DSCR':
                        dependents_names = [group.independent] + group.dependents
                        dependent_types = [group.independentType] + ["complex"]*len(group.dependentsTypes)
                    else:
                        dependents_names = [group.independent] + group.dependents
                        dependent_types = [group.independentType] + ["complex"]*len(group.dependentsTypes)
                    indep_data = block.independent[:, np.newaxis]
                    dep_data = block.dependents
                    if isinstance(indep_data, th.Tensor):
                        indep_data = indep_data.detach().numpy()
                    if isinstance(dep_data, th.Tensor):
                        dep_data = dep_data.detach().numpy()
                    dependents = np.concatenate((indep_data, dep_data), axis=1)

                    f.write('% ')
                    for dependents_name, dependent_type in zip(dependents_names, dependent_types):
                        f.write('%s(%s) '% (dependents_name, dependent_type))
                    f.write('\n')
                    for row in range(dependents.shape[0]):
                        f.write(self._get_string(dependents[row, 0].real, dependent_types[0])
                                + "".join(map(_complex2str, dependents[row, 1:])) + "\n")
                    f.write('END\n\n')

    def _export_dataset(self, ds):
        group = MDIFGroup(name=ds._v_name)
        # Group Sweep
        sweep_map = ds.sweep_map
        for sweep_name, sweep_value in sweep_map.items():
            group.sweeps.append(sweep_name)
            group.sweepTypes.append(MDIF._type_str_map[sweep_value.dtype])

        # Group Independent
        group.independent = group.sweeps.pop(-1)
        group.independentType = group.sweepTypes.pop(-1)

        # Group Dependent
        signal_slice = (slice(None),) * len(ds.shape)
        signal_map = {k: v[signal_slice] for (k, v) in ds._v_children.items() if isinstance(v, SignalArray)}
        for dep_name in signal_map.keys():
            group.dependents.append(dep_name)
            group.dependentsTypes.append("complex")

        step = sweep_map["f"].shape[-1]
        di = ds.__iter__(step, sweep_enabled=False)
        for index, _ in di:
            array_index = di.array_index
            block = MDIFBlock()
            # Block Sweep
            k = 0
            for sweep_value in sweep_map.values():
                sweep_index = [0] * len(array_index)
                sweep_index[k] = array_index[k]
                block.sweep.append(sweep_value[tuple(sweep_index)].reshape(-1))
                k += 1

            # Block Independent
            block.independent = block.sweep.pop(-1)

            # Block Dependent
            block.dependents = np.zeros((len(block.independent), len(signal_map)), dtype=np.complex)
            dep_index = 0
            for dep_name, dep_value in signal_map.items():
                block.dependents[:, dep_index] = dep_value[array_index]
                dep_index += 1
            group.data.append(block)
        self.dataBlocks.append(group)

    @staticmethod
    def write_dataset(dataset, filename):
        """Writes a dataset to an MDIF text file.

        Parameters
        ----------
        dataset : DatasetModel
            Parent datagroup where the resulting dataset is stored.
        filename : str
            MDIF filename.
        """
        root = MDIF(name=os.path.split(filename)[1])
        root._export_dataset(dataset)
        root.write(filename)

    @staticmethod
    def write_datagroup(datagroup, filename):
        """Writes a datagroup to an MDIF text file.

        Parameters
        ----------
        datagroup : DatagroupModel
            Parent datagroup where the resulting dataset is stored.
        filename : str
            MDIF filename.

        """
        root = MDIF(name=os.path.split(filename)[1])
        datasets = [v for v in datagroup.root._v_children.values() if isinstance(v, DatasetModel)]
        for dataset in datasets:
            root._export_dataset(dataset)
        root.write(filename)

    @staticmethod
    def _get_name_type(string):
        """Parse the name(type)
        """
        start_bracket = string.find("(")
        name = string[0:start_bracket]
        type = string[start_bracket+1:-1]
        return name, type

    _str_type_map = {'0': np.int32, 'int': np.int32,
                     '1': np.float64, 'real': np.float64,
                     '2': str, 'string': str,
                     '3': np.complex, 'complex': np.complex,
                     '4': _str2bool, 'boolean': _str2bool,
                     '5': _str2bin, 'binary': _str2bin,
                     '6': _str2oct, 'octal': _str2oct,
                     '7': _str2hex, 'hexadecimal': _str2hex,
                     '8': np.byte, 'byte16': np.byte,
                     }

    _type_str_map = {np.dtype(np.int32): "int",
                     th.int32: "int",
                     np.dtype(np.int64): "int",
                     th.int64: "int",
                     np.dtype(np.float64): "real",
                     th.float64: "real",
                     str: "string",
                     th.complex64: "complex",
                     th.complex128: "complex",
                     }

    _str_value_map = {'0': _int2str, 'int': _int2str,
                      '1': _float2str, 'real': _float2str,
                      '2': str, 'string': str,
                      '3': _complex2str, 'complex': _complex2str,
                      '4': _bool2str, 'boolean': _bool2str,
                      '5': bin, 'binary': bin,
                      '6': oct, 'octal': oct,
                      '7': hex, 'hexadecimal': hex,
                      '8': np.byte, 'byte16': np.byte,
                      }

    @staticmethod
    def _get_value(string, type):
        """Determine the value from the variable string and variable type
        """
        return MDIF._str_type_map[type](string)

    @staticmethod
    def _get_string(value, type):
        """Determine the string from the variable value and variable type
        """
        return MDIF._str_value_map[type](value)
