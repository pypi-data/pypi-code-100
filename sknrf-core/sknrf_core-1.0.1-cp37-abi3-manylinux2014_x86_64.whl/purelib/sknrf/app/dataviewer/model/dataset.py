"""
================================================
Dataset (:mod:`sknrf.model.dataviewer.dataset`)
================================================

This module stores measurement data into a hierarchial HDF5 database consisting of the following organization.

* Datagroup
    * Dataset1
        * v1
        * i1
        * z1
        * ...
    * Dataset2
        * v1
        * i1
        * z1
        * ...
    * ...
    * DatasetN
        * v1
        * i1
        * z1
        * ...

This ensures that related measurement datasets can be stored inside the same database datagroup.

See Also
--------
sknrf.model.dataviewer.equation.EquationModel, sknrf.model.dataviewer.equation.SignalArray

"""
import os
import logging
from itertools import cycle

import re
import numpy as np
import torch as th
import yaml
import tables as tb
from collections import OrderedDict
from tables.node import NotLoggedMixin
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from matplotlib.markers import MarkerStyle
from scipy.signal import resample

from sknrf.app.dataviewer.model.equation import SignalArray, dtype_atom_map
from sknrf.settings import Settings, InstrumentFlag
from sknrf.device.signal import tf
from sknrf.enums.device import Response, rid2b, rid2p
from sknrf.enums.device import response_name_map, response_shape_map, response_fill_map
from sknrf.enums.device import response_dtype_map, response_device_map, response_grad_map
from sknrf.enums.signal import transform_map, transform_label_map, transform_icon_map, transform_xlabel_map
from sknrf.enums.sequencer import Sweep, Goal, sid2b, sid2p
from sknrf.enums.sequencer import sweep_name_map, sweep_shape_map, sweep_fill_map
from sknrf.enums.sequencer import sweep_device_map, sweep_grad_map
from sknrf.device import AbstractDevice
from sknrf.utilities.rf import n2t, t2n, real, imag
from sknrf.utilities.numeric import Domain, unravel_index
from sknrf.icons import black_32_rc

from sknrf.app.dataviewer.model.figure import AxesType, AxisType, PlotType, FormatType, format_map
from sknrf.app.dataviewer.model.figure import AxesModel, PlotModel


__author__ = 'dtbespal'
logger = logging.getLogger(__name__)


def preview_plot(ds, get_func, item: str, filters: list,
                 ax_model: AxesModel, plt_model: PlotModel,
                 transform_type: Domain, options_map):
    format_ = format_map[plt_model.y_format]
    x = y = np.empty((0, 0))
    transform = transform_map[transform_type]
    filters = [f for f in reversed(filters)]
    # Before Transform
    y = get_func(ds, item)[...].detach()
    if isinstance(ds, AbstractDevice):
        if transform_type in (Domain.FT, Domain.TT):
            pad_num = Settings().num_harmonics + 1 - y.shape[-1]
            pad = th.zeros((Settings().t_points, pad_num), dtype=y.dtype)
            if ds.harmonics[0] == Settings().harmonics[0]:  # LF Signal
                y = th.cat((y, pad), dim=-1)
            else:  # RF Signal
                y = th.cat((pad, y), dim=-1)
    y = transform(y)
    for dim, filter_ in enumerate(filters):
        y = y.narrow(dim, filter_[0], filter_[-1] + 1 - filter_[0])

    # After Transform
    if ax_model.type == AxesType.Rectangular:
        y = format_(y)
        if transform_type == Domain.TF:
            x = ds.time[...]
            for dim, filter_ in enumerate(filters):
                if x.shape[dim] > 1:
                    x = x.narrow(dim, filter_[0], filter_[-1] + 1 - filter_[0])
            x = th.moveaxis(x, -2, -1)
            x = x.reshape((-1, x.shape[-1]))
            y = th.moveaxis(y, -2, -1)
            y = y.reshape((th.prod(th.as_tensor(y.shape[:-1])), y.shape[-1]))
        elif transform_type == Domain.FF:
            x = ds.freq_m[...]
            for dim, filter_ in enumerate(filters):
                if x.shape[dim] > 1:
                    x = x.narrow(dim, filter_[0], filter_[-1] + 1 - filter_[0])
            x = th.moveaxis(x, -2, -1)
            x = x.reshape((-1, x.shape[-1]))
            y = th.moveaxis(y, -2, -1)
            y = y.reshape((th.prod(th.as_tensor(y.shape[:-1])), y.shape[-1]))
        elif transform_type == Domain.FT:
            x = ds.time_c[...]
            if len(x.shape) == 1:
                x = x.reshape(1, -1)
            for dim, filter_ in enumerate(filters):
                if x.shape[dim] > 1:
                    x = x.narrow(dim, filter_[0], filter_[-1] + 1 - filter_[0])
            x = x.reshape((-1, x.shape[-1]))
            y = y.reshape((th.prod(th.as_tensor(y.shape[:-1])), y.shape[-1]))
        elif transform_type == Domain.TT:
            x = ds.time_c[...]
            if len(x.shape) == 1:
                x = x.reshape(1, -1)
            for dim, filter_ in enumerate(filters):
                if x.shape[dim] > 1:
                    x = x.narrow(dim, filter_[0], filter_[-1] + 1 - filter_[0])
            x = x.reshape((-1, x.shape[-1]))
            y = y.reshape((th.prod(th.as_tensor(y.shape[:-1])), y.shape[-1]))
    elif ax_model.type == AxesType.Polar:
        x = y.angle()
        x = th.moveaxis(x, -2, -1)
        x = x.reshape((-1, x.shape[-1]))
        y = y.abs()
        y = th.moveaxis(y, -2, -1)
        y = y.reshape((-1, y.shape[-1]))
    elif ax_model.type == AxesType.Smith:
        x = real(y)
        x = th.moveaxis(x, -2, -1)
        x = x.reshape((-1, x.shape[-1]))
        y = imag(y)
        y = th.moveaxis(y, -2, -1)
        y = y.reshape((-1, y.shape[-1]))
    return ax_model, plt_model, x, y, options_map


class WCArray(NotLoggedMixin, tb.Group):
    """Subclass of PyTables CArray desigend to avoid numpy limitation that arrays cannot exceed 32 dimensions"""

    # Class identifier.
    _c_classid = 'WCARRAY'

    def __init__(self, parentnode, name,
                 atom=None, shape=None,
                 title="", new=False, filters=None,
                 chunkshape=None, byteorder=None,
                 _log=True, track_times=True):
        super(WCArray, self).__init__(parentnode, name,
                                      title=title, new=new, filters=filters, _log=_log)
        if new:
            self._v_attrs.name = name
            self._v_attrs.shape = shape
            self._v_attrs.squeeze_shape = tuple([s for s in shape if s > 1])
            tb.CArray(self, name,
                      atom=atom, shape=self._v_attrs.squeeze_shape,
                      title=name, filters=filters,
                      chunkshape=chunkshape, byteorder=byteorder,
                      _log=_log, track_times=track_times)


    def getitem(self, key):
        return th.as_tensor(getattr(self, self._v_attrs.name).__getitem__(key)).reshape(self._v_attrs.shape)

    def __getitem__(self, key):
        return th.as_tensor(getattr(self, self._v_attrs.name).__getitem__(key)).reshape(self._v_attrs.shape)

    def setitem(self, key, value):
        shape = self._v_attrs.squeeze_shape
        if isinstance(key, (list, tuple)):
            key = tuple([k for s, k in zip(self._v_attrs.shape, key) if s > 1])
            shape = tuple([1 if isinstance(k, int) else s for s, k in zip(self._v_attrs.squeeze_shape, key)])
        getattr(self, self._v_attrs.name).__setitem__(key, value.reshape(shape).numpy())

    def __setitem__(self, key, value):
        shape = self._v_attrs.squeeze_shape
        if isinstance(key, (list, tuple)):
            key = tuple([k for s, k in zip(self._v_attrs.shape, key) if s > 1])
            shape = tuple([1 if isinstance(k, int) else s for s, k in zip(self._v_attrs.squeeze_shape, key)])
        getattr(self, self._v_attrs.name).__setitem__(key, value.reshape(shape).numpy())

    def _g_create(self):
        return super(WCArray, self)._g_create()

    def _g_open(self):
        return super(WCArray, self)._g_open()

    def _g_copy(self, newparent, newname, recursive, _log=True, **kwargs):
        return super(WCArray, self)._g_copy(newparent, newname, recursive, _log=_log, **kwargs)


class IQHeader(tb.IsDescription):
    sample_point = tb.UInt32Col(pos=1)
    sample_rate = tb.Float64Col(pos=2)
    waveform_runtime_scaling = tb.Float64Col(pos=3)
    iq_modulation_filter = tb.Float64Col(pos=4)
    iq_output_filter = tb.Float64Col(pos=5)
    marker_1 = tb.StringCol(100, pos=6)
    marker_2 = tb.StringCol(100, pos=7)
    marker_3 = tb.StringCol(100, pos=8)
    marker_4 = tb.StringCol(100, pos=9)
    pulse__rf_blanking = tb.UInt8Col(pos=10)
    alc_hold = tb.UInt8Col(pos=11)
    alc_status = tb.StringCol(10, pos=11)
    bandwidth = tb.StringCol(10, pos=12)
    power_search_reference = tb.StringCol(10, pos=13)


class IQFile(tb.File):
    """Database representation of an IQ Waveform

        Parameters
        ----------
        filename : str
            Absolute filename of the database.
        mode : str
            'r' - read access, 'w' - write access, 'a' - append to existing database.
        title : str
            Title of the node inside the database.

        """

    def __init__(self, filename, *args, mode='r', title='', root_uep='/', filters=None, **kwargs):
        # filters = tb.Filters(complib='blosc', complevel=5)
        super(IQFile, self).__init__(filename=filename, mode=mode, title=title,
                                     root_uep=root_uep, filters=filters, **kwargs)

        t_points = Settings().t_points
        shape = (t_points,)
        if not mode.startswith('r'):
            if len(args) == 0:
                iq_array = np.ones(shape, dtype=np.complex)
                self.create_array(self.root, "iq", iq_array, "Complex IQ Array")
                table = self.create_table(self.root, "header", IQHeader, "Header Table", expectedrows=1)
                header_row = table.row
                header_row["sample_point"] = t_points
                header_row["sample_rate"] = 1/Settings().t_step
                header_row["waveform_runtime_scaling"] = 1.0
                header_row["iq_modulation_filter"] = 40.0e6
                header_row["iq_output_filter"] = 40.0e6
                header_row["marker_1"] = "None"
                header_row["marker_2"] = "None"
                header_row["marker_3"] = "None"
                header_row["marker_4"] = "None"
                header_row["pulse__rf_blanking"] = 4
                header_row["alc_hold"] = 4
                header_row["alc_status"] = "Off"
                header_row["bandwidth"] = "Auto"
                header_row["power_search_reference"] = "Modulation"
                header_row.append()
                table.flush()
            else:
                iq_array, header_map = args[0], args[1]
                self.create_array(self.root, "iq", iq_array, "Complex IQ Array")
                table = self.create_table(self.root, "header", IQHeader, "Header Table", expectedrows=1)
                header_row = table.row
                for k, v in header_map.items():
                    header_row[k] = v
                header_row.append()
                table.flush()

    @property
    def iq(self):
        t_step, t_points = Settings().t_step, Settings().t_points
        if self.filename.endswith("CW.h5"):
            upsample_factor = 1
        else:
            upsample_factor = int(np.ceil(1/t_step/self.header["sample_rate"]))
        iq_array = self.root.iq[...]
        iq_array = resample(iq_array, upsample_factor*iq_array.size)
        if t_points <= iq_array.size:
            iq_array = iq_array[0:t_points]
        else:
            iq_array = np.append(np.tile(iq_array, (int(np.floor(t_points / iq_array.size)),)),
                                 iq_array[0:np.mod(t_points, iq_array.size)])
        return n2t(iq_array)

    @property
    def header(self):
        header_map = OrderedDict()
        header_row = self.root.header.iterrows().__next__()
        for k in self.root.header.colnames:
            try:
                v = header_row[k].decode()
                if len(v) == 0:
                    v = "None"
            except AttributeError:
                v = header_row[k]
            header_map[k] = v
        return header_map

    @property
    def marker(self):
        t_step, t_points = Settings().t_step, Settings().t_points
        if self.filename.endswith("CW.h5"):
            upsample_factor = 1
        else:
            upsample_factor = int(np.ceil(1/t_step/self.header["sample_rate"]))
        header_row = self.root.header.iterrows().__next__()
        m = np.zeros((t_points,), dtype=">i1")
        for marker_index in range(0, 4):
            marker_name = "marker_%d" % (marker_index + 1,)
            marker_str = header_row[marker_name].decode()
            if marker_str.lower() == "none":
                m |= np.left_shift(0, marker_index)
            elif marker_str.lower() == "all":
                m |= np.left_shift(1, marker_index)
            elif len(marker_str) != 0:
                segments = marker_str.split(", ")
                for segment in segments:
                    start, stop = segment.strip().split("-")
                    start_val, stop_val = upsample_factor*(int(start.strip()) - 1), upsample_factor*int(stop.strip())
                    m[start_val:stop_val] |= np.left_shift(1, marker_index)

        if t_points <= m.size:
            m = m[0:t_points]
        else:
            m = np.append(np.tile(m, (int(np.floor(t_points / m.size)),)),
                          m[0:np.mod(t_points, m.size)])
        return n2t(m)

    @staticmethod
    def from_waveform(filename, iq_array, header_map):
        iq_array = iq_array[0::2] + 1j*iq_array[1::2]
        iq_array = iq_array.astype(np.complex)
        return IQFile(filename, iq_array, header_map, mode='w')

    def to_waveform(self):
        iq_array = t2n(self.iq)
        iq_array.dtype = np.float  # Interleave IQ
        iq_array = np.round(iq_array*(32767/np.max(np.abs(iq_array))))  # Scaling
        iq_array = iq_array.astype(">i2")  # Convert to big endian uint16.
        return iq_array, self.header, t2n(self.marker).astype(np.int8)

    @staticmethod
    def from_txt(filename, i_filename, q_filename, config_filename):
        iq_array = np.loadtxt(i_filename, delimiter='\r\n', dtype=np.complex) \
                   + 1j * np.loadtxt(q_filename, delimiter='\r\n', dtype=np.complex)
        with open(config_filename, "rt") as f:
            while not f.readline().startswith("### Don't Touch ###"):
                pass
            header_map = yaml.full_load(f)
            for k in list(header_map.keys()):
                k_list = re.split("\s+", k)
                k_, unit = ("_".join(k_list[:-1]), k_list[-1][1:-1]) if k_list[-1][0] == '(' else ("_".join(k_list), "")
                k_ = k_.lower().replace('/', "__")
                v = header_map.pop(k)
                try:
                    if unit == "MHz":
                        v *= 1e6
                    elif unit == "%":
                        v /= 100
                except TypeError:
                    v = np.nan
                header_map[k_] = v
        return IQFile(filename, iq_array, header_map, mode='w')

    def to_txt(self, i_filename, q_filename, config_filename):
        iq_array = self.iq
        np.savetxt(i_filename, iq_array.real)
        np.savetxt(q_filename, iq_array.imag)
        with open(config_filename, "wt") as f:
            f.write("### Don't Touch ###\n")
            f.write("\n")
            yaml.dump(dict(self.header), f, default_flow_style=False)

    def tostring(self):
        iq_array = t2n(self.iq)
        iq_array.dtype = np.float
        return iq_array.astype(">i2").tostring()

    def _g_create(self):
        return super(IQFile, self).create()

    def _g_open(self):
        return super(IQFile, self)._g_open()

    def _g_copy(self, newparent, newname, recursive, _log=True, **kwargs):
        return super(IQFile, self)._g_copy(newparent, newname, recursive, _log=_log, **kwargs)


class DatasetIterator(object):

    def __init__(self, dataset, step=1, sweep_enabled=True):
        self.dataset = dataset
        self.sweep_enabled = sweep_enabled
        self.sweep_map = dataset.sweep_map
        self.shape = list(dataset.shape)
        self.slice_index = []
        while self.shape and not step % self.shape[-1]:
            step = int(step / self.shape[-1])
            del self.shape[-1]
            self.slice_index.append(slice(None))
        self.shape = tuple(self.shape)
        self.slice_index = tuple(self.slice_index)
        self.array_index = self.slice_index
        self.i = 0
        self.n = int(np.prod(self.shape))

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < self.n:
            self.array_index = unravel_index(self.i, self.shape) + self.slice_index
            i = self.i
            ds = self.dataset
            viz_bag = [None]*(Settings().num_ports + 1)
            step_shape = (-1, ds.shape[-1])
            if self.sweep_enabled:
                for port_index in range(Settings().num_ports + 1):
                    if port_index in ds.ports:
                        lf_index = self.array_index[0:-1] + (slice(0, 1),)
                        zg = getattr(ds, sid2p(Sweep.Z_SET, port_index, 0))[...][lf_index]
                        vb = getattr(ds, sid2p(Sweep.V_SET, port_index, 0))[...][lf_index]
                        ia = th.zeros_like(zg)
                        for harm_index in range(1, Settings().f_points):
                            rf_index = self.array_index[0:-1] + (slice(harm_index, harm_index+1),)
                            g = getattr(ds, sid2p(Sweep.G_SET, port_index, harm_index))[...][rf_index]
                            b = th.zeros_like(g)
                            a = getattr(ds, sid2p(Sweep.A_SET, port_index, harm_index))[...][rf_index]
                            vb, ia, zg = th.cat((vb, b), -1), th.cat((ia, a), -1), th.cat((zg, g), -1)
                        viz_bag[port_index] = [vb.reshape(step_shape), ia.reshape(step_shape), zg.reshape(step_shape)]
            self.i += 1
            return i, viz_bag
        else:
            raise StopIteration()

    def save(self, viz_bag, aux):
        ds = self.dataset
        num_harmonics = Settings().num_harmonics
        array_index = self.array_index
        array_shape = tuple([shape if isinstance(index, slice) else 1 for index, shape in zip(array_index, ds.shape)])

        if ds.ports[-1] == 2 and viz_bag[2] is None:
            print("wtf")

        for port_index in ds.ports:
            vb, ia, zg = viz_bag[port_index]
            shape_ = array_shape[0:-1] + (num_harmonics + 1,)
            vb = vb.detach().reshape(shape_)
            ia = ia.detach().reshape(shape_)
            zg = zg.detach().reshape(shape_)
            getattr(ds, rid2p(Response.V_GET, port_index)).__setitem__(array_index, vb)
            getattr(ds, rid2p(Response.I_GET, port_index)).__setitem__(array_index, ia)
            getattr(ds, rid2p(Response.Z_GET, port_index)).__setitem__(array_index, zg)
            getattr(ds, rid2p(Response.B_GET, port_index)).__setitem__(array_index, vb)
            getattr(ds, rid2p(Response.A_GET, port_index)).__setitem__(array_index, ia)
            getattr(ds, rid2p(Response.G_GET, port_index)).__setitem__(array_index, zg)
        array_index = self.array_index[0:-2] + (slice(None, ),)*3
        array_shape = array_shape[0:-2]
        freq, pm, sa, sp = aux
        freq = freq.detach().reshape(array_shape + response_shape_map[Response.SS_FREQ])
        pm = pm.detach().reshape(array_shape + response_shape_map[Response.P])
        sa = sa.detach().reshape(array_shape + response_shape_map[Response.PSD])
        sp = sp.detach().reshape(array_shape + response_shape_map[Response.SP])
        # getattr(ds, rid2p(Response.SS_FREQ)).__setitem__(array_index, freq)
        # getattr(ds, rid2p(Response.P)).__setitem__(array_index, pm)
        # getattr(ds, rid2p(Response.PSD)).__setitem__(array_index, sa)
        # getattr(ds, rid2p(Response.SP)).__setitem__(array_index, sp)


class DatasetModel(NotLoggedMixin, tb.Group):
    """Database representation of a Dataset

    Parameters
    ----------
    parentnode : tables.File
        Reference the parent node inside the database.
    name : str
        Database node name.
    sweep_map : OrderedDict
        Parametric sweeps stored inside the dataset.
    indep_map : OrderedDict
        Independent sweeps stored inside the dataset.
    title : str
        Database node name
    new : bool
        Create new node in database if True.
    filters : tables.Filters
        A filters instance.
    _log : bool

    """
    _c_classid = 'DATASETMODEL'

    def __init__(self, parentnode, name, ports=tuple(), duts=tuple(), mipis=tuple(), videos=tuple(),
                 sweep_map=OrderedDict(), indep_map=OrderedDict(),
                 title='', new=False, filters=None, _log=True):
        name = name.strip("/")
        super(DatasetModel, self).__init__(parentnode, name, title=title, new=new, filters=filters, _log=_log)
        if new:
            sweep_names = []
            sweep_shape = []
            for index, (k, v) in enumerate(reversed(sweep_map.items())):
                sweep_names.append(k.encode('utf-8'))
                sweep_shape.append(v.shape[index])
            self._v_attrs.ports = ports if len(ports) else tuple(range(0, Settings().num_ports+1))
            self._v_attrs.duts = duts if len(duts) else tuple(range(0, Settings().num_duts))
            self._v_attrs.mipis = mipis if len(mipis) else tuple(range(0, Settings().num_mipi))
            self._v_attrs.videos = videos if len(videos) else tuple(range(0, Settings().num_video))
            self._v_attrs.sweep_names = sweep_names
            self._v_attrs.sweep_shape = sweep_shape
            for index, (k, v) in enumerate(reversed(sweep_map.items())):
                WCArray(self, k, atom=dtype_atom_map[v.dtype], shape=sweep_shape, new=new, filters=filters)
                fill = th.zeros(sweep_shape, dtype=v.dtype)
                getattr(self, k)[...] = v.detach() + fill
            self._sweep_map = sweep_map
            for index, (k, v) in enumerate(reversed(indep_map.items())):
                fill_shape = [1]*(len(sweep_shape))
                fill_shape[-len(v.shape)] = v.numel()
                WCArray(self, k, atom=dtype_atom_map[v.dtype], shape=fill_shape, new=new, filters=filters)
                getattr(self, k)[...] = v.reshape(fill_shape).detach()
            self._indep_map = indep_map

            for resp_id in (Response.V_GET, Response.I_GET, Response.Z_GET, Response.B_GET, Response.A_GET, Response.G_GET):
                for port_index in self._v_attrs.ports:
                    k = rid2p(resp_id, port_index)
                    resp_shape = sweep_shape[0:-2] + list(response_shape_map[resp_id])
                    atom = dtype_atom_map[response_dtype_map[resp_id]]
                    WCArray(self, k, atom=atom, shape=resp_shape, new=new, filters=filters)
                    getattr(self, k)[...] = th.zeros(resp_shape, dtype=response_dtype_map[resp_id]).detach()

            if "sp_fund" in self and "sp_harm" in self and "sp_port" in self:
                # (sp_harm*sp_fund, sp_port, sp_port)
                k = 's'
                s_shape = th.prod(th.as_tensor(self.shape[-4:-2])), self.shape[-5], self.shape[-5]
                WCArray(self, k, atom=tb.ComplexAtom(16), shape=s_shape, title=k, new=new)
                getattr(self, k)[...] = th.zeros(s_shape, dtype=th.complex128).detach()

            # for resp_id in (Response.VIDEO, Response.TEMP):
            #     for dut_index in self._v_attrs.duts:
            #         resp_shape = sweep_shape[0:-2] + list(response_shape_map[resp_id])
            #         atom = dtype_atom_map[response_dtype_map[resp_id]]
            #         CArray(self, rid2p(resp_id, dut_index), atom=atom, shape=resp_shape, new=new, filters=filters)
            #
            # for resp_id in (Response.SS_FREQ, Response.P, Response.PSD, Response.SP):
            #     resp_shape = sweep_shape[0:-2] + list(response_shape_map[resp_id])
            #     atom = dtype_atom_map[response_dtype_map[resp_id]]
            #     CArray(self, rid2p(resp_id), atom=atom, shape=resp_shape, new=new, filters=filters)
        else:
            names = self._v_attrs.sweep_names
            sweeps = [(k.decode('utf-8'), getattr(self, k.decode('utf-8'))[...]) for k in names]
            self._sweep_map = OrderedDict(sweeps)

    def __iter__(self, step, sweep_enabled=True):
        return DatasetIterator(self, step, sweep_enabled=sweep_enabled)

    @property
    def sweep_map(self):
        return self._sweep_map

    @property
    def indep_map(self):
        return self._indep_map

    @property
    def shape(self):
        return self._v_attrs.sweep_shape

    @property
    def ports(self):
        return self._v_attrs.ports

    @property
    def duts(self):
        return self._v_attrs.duts

    @property
    def videos(self):
        return self._v_attrs.videos

    def add(self, name, value):
        """ Add new dataset.

        Parameters
        ----------
        name : str
            Equation name.
        value : EnvelopeSignal
            Equation value.

        Returns
        -------
        SignalArray
            The database reference to the value.

        """
        if name in list(self._v_children.keys()):
            raise AttributeError("The dataset equation already exists")
        eq = SignalArray(self, name, value, new=True)
        return eq

    def has_equation(self, name):
        """ Returns true if dataset has existing equation name.

        Parameters
        ----------
        name : str
            Equation name.

        Returns
        -------
        bool
            True if dataset has equation name, else False.

        """
        return self.__contains__(name)

    def equation(self, name):
        """ Gets the equation by name.

        Parameters
        ----------
        name : str
            Equation name.

        Returns
        -------
        SignalArray
            The selected equation.

        """
        return self._f_get_child(name)

    def set_equation(self, name, value):
        """ Sets the equation by name.

        Parameters
        ----------
        name : str
            Equation name.
        value : EnvelopeSignal
            Equation value.

        """
        self._f_get_child(name)[...] = value

    def rename(self, old_name, new_name, overwrite=False):
        """ Rename the equation from old_name to new_name

        Parameters
        ----------
        old_name : str
            Old dataset name.
        new_name : str
            New dataset Name.
        overwrite : bool
            Overwrite an existing dataset if necessary.

        """
        self._f_get_child(old_name)._f_rename(new_name, overwrite=overwrite)

    def remove(self, name):
        """ Remove the equation by name.

        Parameters
        ----------
        name : str
            Equation name.

        """
        return self._f_get_child(name)._f_remove(name, force=True)

    def _g_create(self):
        return super(DatasetModel, self)._g_create()

    def _g_open(self):
        return super(DatasetModel, self)._g_open()

    def _g_copy(self, newparent, newname, recursive, _log=True, **kwargs):
        return super(DatasetModel, self)._g_copy(newparent, newname, recursive, _log=_log, **kwargs)


class DatagroupModel(tb.File):
    """Database representation of a Datagroup

    Parameters
    ----------
    filename : str
        Absolute filename of the database.
    mode : str
        'r' - read access, 'w' - write access, 'a' - append to existing database.
    title : str
        Title of the node inside the database.

    """

    def __init__(self, filename="", mode='r', title='', root_uep='/', filters=None, **kwargs):
        filters = tb.Filters(complib='blosc', complevel=5) if filters is None else filters
        if not filename:
            filename = os.sep.join([Settings().data_root, "datagroups", Settings().datagroup + ".h5"])
        file_exists = os.path.isfile(filename)
        super(DatagroupModel, self).__init__(filename=filename, mode=mode, title=title,
                                             root_uep=root_uep, filters=filters, **kwargs)
        if file_exists:
            try:
                str(self.root)
            except:
                self.close()
                os.remove(filename)
                super(DatagroupModel, self).__init__(filename=filename, mode=mode, title=title,
                                                     root_uep=root_uep, filters=filters, **kwargs)

    def add(self, name, ports=tuple(), duts=tuple(), mipis=tuple(), videos=tuple(),
            sweep_map=OrderedDict(), indep_map=OrderedDict(),
            title='', filters=None, _log=True):
        """ Add new dataset.

        Parameters
        ----------
        name : str
            Dataset name.
        indep_map : IndepDict
            Parametric sweeps stored inside the dataset.
        title : str
            Title of the node inside the database.
        filters : tables.Filters
            A filters instance.
        _log : bool

        """
        filters = tb.Filters(complib='blosc', complevel=5) if filters is None else filters
        return DatasetModel(self.root, name, ports=ports, duts=duts, mipis=mipis, videos=videos,
                            sweep_map=sweep_map, indep_map=indep_map,
                            title=title, new=True, filters=filters, _log=_log)

    def has_dataset(self, name):
        """ Returns true if datagroup has existing dataset name.

        Parameters
        ----------
        name : str
            Dataset name.

        Returns
        -------
        bool
            True if datagroup has dataset name, else False.

        """
        return self.root.__contains__(name)

    def dataset(self, name):
        """ Gets the dataset by name.

        Parameters
        ----------
        name : str
            Dataset name.

        Returns
        -------
        DatasetModel
            The selected dataset.

        """
        return self.root._f_get_child(name)

    def rename(self, old_name, new_name, overwrite=False):
        """ Rename the dataset from old_name to new_name

        Parameters
        ----------
        old_name : str
            Old dataset name.
        new_name : str
            New dataset Name.
        overwrite : bool
            Overwrite an existing dataset if necessary.

        """
        self.rename_node(self.root, new_name, old_name, overwrite=overwrite)

    def remove(self, name):
        """ Remove the dataset by name.

        Parameters
        ----------
        name : str
            Dataset name.

        """
        self.remove_node(self.root, name, recursive=True)

    def _g_create(self):
        return super(DatagroupModel, self).create()

    def _g_open(self):
        return super(DatagroupModel, self)._g_open()

    def _g_copy(self, newparent, newname, recursive, _log=True, **kwargs):
        return super(DatagroupModel, self)._g_copy(newparent, newname, recursive, _log=_log, **kwargs)


class DatagroupTreeModel(QStandardItemModel):
    """The equation table Model.

        Parameters
        ----------
        root : OrderedDict
            The dictionary of items that populate the equation table.
    """
    def __init__(self, parent=None, root={}):
        super(DatagroupTreeModel, self).__init__(parent)
        self.header = ['Datagroups']
        self._root = root
        self._selected_names = []
        self._selected_values = []
        self._selected_markers = []
        self.__marker_cycle = cycle(MarkerStyle.filled_markers)
        for k, v in self._root.keys():
            self.appendRow(k, v)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def flags(self, index):
        if index.child(0, 0).row() == -1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled

    def appendRow(self, dg_name, dg, dg_model):
        base_name = dg_name
        count = 0
        dg_name = base_name
        while dg_name in dg_model:
            count += 1
            dg_name = "%s%d" % (base_name, count)
        dg_item = QStandardItem(dg_name)
        super(DatagroupTreeModel, self).appendRow(dg_item)
        for ds_name, ds in dg.root._v_children.items():
            if not ds_name.startswith("_"):
                name = ".".join((dg_name, ds_name))
                marker = self.__marker_cycle.__next__()
                icon_filename = os.sep.join((Settings().root, "icons/markers/", MarkerStyle.markers[marker] + ".png"))
                ds_item = QStandardItem(QIcon(icon_filename), ds_name)
                ds_item.setData(marker, Qt.UserRole)
                dg_item.appendRow(ds_item)
                self._root[name] = ds
        dg_model[dg_name] = dg

    def removeRow(self, index, parent, dg_model):
        dg_name = index.data(Qt.DisplayRole)
        super(DatagroupTreeModel, self).removeRow(index.row(), parent)
        for ds_name, ds in dg_model[dg_name].root._v_children.items():
            if not ds_name.startswith("_"):
                name = ".".join((dg_name, ds_name))
                self._root.pop(name)
        dg_model[dg_name].close()
        dg_model.pop(dg_name)

    def selected(self):
        """
            Returns
            -------
            ndarray
                The selected dictionary value based on the selected row.
        """
        return self._selected_names, self._selected_values, self._selected_markers

    @QtCore.Slot(int)
    def set_selected(self, indices):
        """ Set the selected dictionary value

            Parameters
            ----------
            index : QtCore.QModelIndex
                The table row to be selected.
        """
        self._selected_names.clear(), self._selected_values.clear(), self._selected_markers.clear()
        for index in indices:
            item = self.itemFromIndex(index)
            name = ".".join((item.parent().text(), item.text()))
            self._selected_names.append(name)
            self._selected_values.append(self._root[name])
            self._selected_markers.append(index.data(Qt.UserRole))


