import os
import time
import datetime
from collections import OrderedDict

import numpy as np
from scipy.io import loadmat, savemat

from sknrf.app.dataviewer.model.dataset import DatagroupModel, DatasetModel


class MATGroup(object):
    """A group of MDIF Blocks.

        Attributes
        ----------
        sweeps : OrderedDict
            dictionary of sweeps.
        attributes : OrderedDict
            dictionary of attributes.
        values : OrderedDict
            dictionary of measurement values.
    """
    def __init__(self, name, sweeps=OrderedDict(), attributes=OrderedDict(), values=OrderedDict()):
        super(MATGroup, self).__init__()
        self.name = name
        self.sweeps = sweeps
        self.attributes = attributes
        self.values = values


class MAT(object):
    """MAT data container.

        Attributes
        ----------
        name : str
            filename.
        date : str
            date/time of creation.
        dataBlocks : list
            list of MDIF Groups containing measurement types.
    """

    def __init__(self, name="", dataBlocks=None):
        super(MAT, self).__init__()
        path, filename = os.path.split(name)
        date_time = os.path.getctime(name) if path else time.time()
        date_str = datetime.datetime.fromtimestamp(date_time).strftime('%Y-%m-%d %H:%M:%S')
        self.name = filename
        self.date = date_str
        self.dataBlocks = dataBlocks if dataBlocks else OrderedDict()

    @staticmethod
    def read(filename):
        """Read an MDIF file and store it inside an MDIF container.

            Parameters
            ----------
            filename : str
                filename.
        """
        root = MAT(name=filename)
        mat = loadmat(filename)
        reserved_names = ["__globals__", "__header__", "__version__", "data", "name"]
        group_names = [group_name for group_name in mat.keys() if group_name not in reserved_names]
        for group_name in group_names:
            group = mat[group_name]
            sweeps, attributes, values = OrderedDict(), OrderedDict(), OrderedDict()
            mat_sweeps, mat_attributes, mat_values = group[0, 0]["sweeps"][0, 0], group[0, 0]["attributes"][0, 0], group[0, 0]["values"][0, 0]
            if mat_sweeps is not None:
                for sweep_name in mat_sweeps.dtype.names:
                    sweeps[sweep_name] = mat_sweeps[sweep_name].astype(np.complex)
            if mat_attributes is not None:
                for attribute_name in mat_attributes.dtype.names:
                    attributes[attribute_name] = mat_attributes[attribute_name].astype(np.complex)
            if mat_values is not None:
                for value_name in mat_values.dtype.names:
                    values[value_name] = mat_values[value_name].astype(np.complex)
            root.dataBlocks[group_name] = MATGroup(group_name, sweeps=sweeps, attributes=attributes, values=values)
        return root

    @staticmethod
    def import_dataset(filename, group_name, num_ports=1, class_=None):
        """Import an MDIF file into a Dataset.

            Parameters
            ----------
            filename : str
                filename.
            group_name : str
                MDIF Group name.
            num_ports : int
                Number of ports inside the dataset.
            class_ : object
                type cast applied to MDIF container to support derived classes.
        """
        if class_:
            root = class_.read(filename)
        else:
            root = MAT.read(filename)
        dataset = Dataset(group_name)
        group = root.dataBlocks[group_name]
        dataset.sweeps = group.sweeps
        dataset.attributes = group.attributes
        dataset.values = group.values
        return dataset

    @staticmethod
    def export_dataset(dataset, filename, group_name, mode='w', subset=Ellipsis):
        if not isinstance(dataset, Dataset):
            raise TypeError("Expected Dataset Type")
        root = MAT()
        group = MATGroup(group_name, sweeps=dataset.sweeps, attributes=dataset.attributes, values=dataset.values)
        root.dataBlocks[group_name] = group
        root.write(filename, mode=mode)

    def write(self, filename, mode='w', do_compression=False):
        """Write an MDIF container to a file.

            Parameters
            ----------
            filename : str
                filename.
            mode : str
                write ('w') or append ('a')
            do_compression : bool
                enable data compression. Default is False.
        """
        root = OrderedDict()
        root["name"] = self.name
        root["data"] = self.date
        for group_name, group in self.dataBlocks.items():
            sweeps = OrderedDict()
            attributes = OrderedDict()
            values = OrderedDict()
            for sweep_name, sweep in group.sweeps.items():
                sweeps[sweep_name.lstrip("_")] = sweep
            for attribute_name, attribute in group.attributes.items():
                attributes[attribute_name.lstrip("_")] = attribute
            for value_name, value in group.values.items():
                values[value_name.lstrip("_")] = value
            root[group_name] = OrderedDict((("sweeps", sweeps),
                                            ("attributes", attributes),
                                            ("values", values)))
        append = True if mode == 'a' else False
        savemat(filename, root, appendmat=True, do_compression=do_compression, oned_as='column')



if __name__ == '__main__':
    from sknrf.settings import Settings
    from sknrf.app.dataviewer.model.mdif import MDIF
    print(Settings().data_root)
    mdif_filename = os.sep.join((Settings().data_root, "datasets", "dataset.mdf"))
    mat_filename = os.sep.join((Settings().data_root, "datasets", "dataset.mat"))
    dataset_ = MDIF.import_dataset(mdif_filename, "WaveData")
    MAT.export_dataset(dataset_, mat_filename, "WaveData", mode="w")
    dataset_ = MAT.import_dataset(mat_filename, "WaveData")
    # a = 1