import sys
from collections import OrderedDict

import torch as th
from torch.nn import Parameter, Module, Sequential
from pyvisa.resources import Resource

from sknrf.settings import Settings, DeviceFlag, device_name_map
from sknrf.device.simulator.base import AbstractSimulator
from sknrf.device.instrument.lfsource.base import NoLFSource
from sknrf.device.instrument.lfreceiver.base import NoLFReceiver
from sknrf.device.instrument.lfztuner.base import NoLFZTuner
from sknrf.device.instrument.rfsource.base import NoRFSource
from sknrf.device.instrument.rfreceiver.base import NoRFReceiver
from sknrf.device.instrument.rfztuner.base import NoRFZTuner
from sknrf.device.dut.base import NoDUT
from sknrf.device.dut.mipi.server.base import NoMIPIServer
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.dut.video.base import NoVideo
from sknrf.device.instrument.auxiliary.pm.base import NoPM
from sknrf.device.instrument.auxiliary.sa.base import NoSA
from sknrf.device.instrument.auxiliary.vna.base import NoVNA
from sknrf.device.signal import tf, ff
from sknrf.enums.device import Response, rid2b, rid2p
from sknrf.enums.device import response_shape_map, response_fill_map
from sknrf.enums.device import response_dtype_map, response_device_map, response_grad_map
from sknrf.enums.sequencer import Sweep, sid2b, sid2p
from sknrf.enums.sequencer import sweep_shape_map, sweep_fill_map
from sknrf.enums.sequencer import sweep_dtype_map, sweep_device_map
from sknrf.utilities.rf import baz2viz, viz2baz, g2z, z2g

if sys.platform == "win32":
    import pythoncom
    from win32com.client import Dispatch

__author__ = 'dtbespal'


class TransformModel(Sequential):

    def append(self, key, value):
        keys = list(self._modules.keys())
        values = list(self._modules.values())
        keys.append(self.mangle(key))
        values.append(value)
        self.clear()
        self.__init__(OrderedDict(zip(keys, values)))

    def pop(self, key):
        value = self._modules.pop(key)
        keys = list(self._modules.keys())
        values = list(self._modules.values())
        self.__init__(OrderedDict(zip(keys, values)))
        return value

    def insert(self, idx, key, value):
        keys = list(self._modules.keys())
        values = list(self._modules.values())
        keys.insert(idx, self.mangle(key))
        values.insert(idx, value)
        self.clear()
        self.__init__(OrderedDict(zip(keys, values)))

    def remove(self, idx):
        del self[idx]

    def mangle(self, key):
        index = 1
        new_key = key
        while new_key in self._modules.keys():
            new_key = "%s%d" % (key, index)
        return new_key

    def clear(self):
        for idx in reversed(range(len(self._modules))):
            del self[idx]


class ErrorModel(Module):

    def __init__(self, num_ports, num_duts, num_mipi, num_video, sweep_step, old_model=None):
        super().__init__()
        self.sweep_step = sweep_step
        if old_model is None or sweep_step != 1:
            self.register_buffers(num_ports, num_duts, num_mipi, num_video)
            self.register_parameters(num_ports, num_duts, num_mipi, num_video)
        else:  # Copy the end of the last measurement
            for k, v in old_model._buffers.items():
                self.register_buffer(k, v[-Settings().t_points::, ...])
            for k, v in old_model._parameters.items():
                self.register_parameter(k, Parameter(v[-Settings().t_points::, ...]))
        self.transforms = TransformModel()

    def register_buffers(self, num_ports, num_duts, num_mipi, num_video):
        for resp_id in (Response.V_GET, Response.I_GET, Response.Z_GET, Response.B_GET, Response.A_GET, Response.G_GET):
            for port_index in range(num_ports+1):
                resp_shape = list(response_shape_map[resp_id])
                resp_shape[0] *= self.sweep_step
                if resp_id & Response.Z_GET or resp_id & Response.G_GET:
                    value = tf.delta(resp_shape, response_fill_map[resp_id])
                else:
                    value = th.full(resp_shape, response_fill_map[resp_id],
                                    dtype=response_dtype_map[resp_id], device=response_device_map[resp_id])
                self.register_buffer(rid2b(resp_id, port_index), value)

        for sweep_id in (Sweep.V_SET, Sweep.I_SET, Sweep.Z_SET, Sweep.B_SET, Sweep.A_SET, Sweep.G_SET):
            for port_index in range(num_ports+1):
                sweep_shape = list(sweep_shape_map[sweep_id])
                sweep_shape[0] *= self.sweep_step
                if sweep_id & Sweep.Z_SET or sweep_id & Sweep.G_SET:
                    value = tf.delta(sweep_shape, sweep_fill_map[sweep_id])
                else:
                    value = th.full(sweep_shape, sweep_fill_map[sweep_id],
                                    dtype=sweep_dtype_map[sweep_id], device=sweep_device_map[sweep_id])
                self.register_buffer(sid2b(sweep_id, port_index), value)

    def register_parameters(self, num_ports, num_duts, num_mipi, num_video):
        resp_ids = (Response.V_GET, Response.I_GET, Response.Z_GET, Response.B_GET, Response.A_GET, Response.G_GET)
        for port_index in range(num_ports+1):
            for resp_id in resp_ids:
                resp_shape = list(response_shape_map[resp_id])
                resp_shape[0] *= self.sweep_step
                if resp_id & Response.Z_GET or resp_id & Response.G_GET:
                    value = tf.delta(resp_shape, response_fill_map[resp_id])
                else:
                    value = th.full(resp_shape, response_fill_map[resp_id],
                                    dtype=response_dtype_map[resp_id], device=response_device_map[resp_id],
                                    requires_grad=response_grad_map[resp_id])
                self.register_parameter(rid2p(resp_id, port_index), Parameter(value))

        for dut_index in range(num_duts):
            for resp_id in (Response.TEMP,):
                resp_shape = list(response_shape_map[resp_id])
                resp_shape[0] *= self.sweep_step
                value = th.full(resp_shape, response_fill_map[resp_id],
                                dtype=response_dtype_map[resp_id], device=response_device_map[resp_id],
                                requires_grad=response_grad_map[resp_id])
                self.register_parameter(rid2p(resp_id, dut_index), Parameter(value))
            for mipi_index in range(num_mipi):
                pass
            for video_index in range(num_video):
                for resp_id in (Response.VIDEO,):
                    resp_shape = list(response_shape_map[resp_id])
                    resp_shape[0] *= self.sweep_step
                    value = th.full(resp_shape, response_fill_map[resp_id],
                                    dtype=response_dtype_map[resp_id], device=response_device_map[resp_id],
                                    requires_grad=response_grad_map[resp_id])
                    self.register_parameter(rid2p(resp_id, dut_index, video_index), Parameter(value))

        for resp_id in (Response.SS_FREQ, Response.P, Response.PSD, Response.SP):
            resp_shape = list(response_shape_map[resp_id])
            resp_shape[0] *= self.sweep_step
            value = th.full(resp_shape, response_fill_map[resp_id],
                            dtype=response_dtype_map[resp_id], device=response_device_map[resp_id])
            self.register_parameter(rid2p(resp_id), Parameter(value))

        for sweep_id in (Sweep.V_SET, Sweep.I_SET, Sweep.Z_SET, Sweep.B_SET, Sweep.A_SET, Sweep.G_SET):
            for port_index in range(num_ports+1):
                sweep_shape = list(sweep_shape_map[sweep_id])
                sweep_shape[0] *= self.sweep_step
                if sweep_id & Sweep.Z_SET or sweep_id & Sweep.G_SET:
                    value = tf.delta(sweep_shape, sweep_fill_map[sweep_id])
                else:
                    value = th.full(sweep_shape, sweep_fill_map[sweep_id],
                                    dtype=sweep_dtype_map[sweep_id], device=sweep_device_map[sweep_id])
                self.register_parameter(sid2p(sweep_id, port_index), Parameter(value))


class PortModel(object):
    """A collection of all device objects connected to a given port

        Args:
            port_num (int): The measurement test-bench port number
    """

    def __init__(self, error_model, port_num):
        super(PortModel, self).__init__()
        self.port_num = port_num
        self.lfsource = NoLFSource(error_model, port_num)
        self.lfreceiver = NoLFReceiver(error_model, port_num)
        self.lfztuner = NoLFZTuner(error_model, port_num)
        self.rfsource = NoRFSource(error_model, port_num)
        self.rfreceiver = NoRFReceiver(error_model, port_num)
        self.rfztuner = NoRFZTuner(error_model, port_num)

    def set_instrument(self, device_name, instrument):
        setattr(self, device_name, instrument)


class DevicesModel(object):
    """A container that contains references to all connected device

        Args:
            num_ports (int): The number of ports in measurement test-bench.
            num_duts (int): The number of DUTs in measurement test-bench.
    """

    def __new__(cls, num_ports, num_duts, num_mipi, num_video, error_model=None):
        self = super(DevicesModel, cls).__new__(cls)
        self._handle_ref_map = {}
        self._marshall_map = {}
        self.ports = []
        self.aux = [None]*3
        self.duts = []
        self._step = Settings().t_points*Settings().f_points
        self._sweep_step = 1
        self.error_model = error_model
        return self

    def __getnewargs__(self):
        return len(self.ports) - 1, len(self.duts), len(self.duts[0].mipi), len(self.duts[0].video), self.error_model

    def __init__(self, num_ports, num_duts, num_mipi, num_video, error_model=None):
        super(DevicesModel, self).__init__()
        self.error_model = ErrorModel(num_ports, num_duts, num_mipi, num_video, self._sweep_step)
        self.ports = [PortModel(self, i) for i in range(0, num_ports+1)]
        self.duts = [NoDUT(self, i) for i in range(num_duts)]
        self.aux = [NoPM(self, num_ports), NoSA(self, num_ports),  NoVNA(self, num_ports)]
        self.transforms = TransformModel()
        self.stimulus()
        self.measure()

    def __getstate__(self, state={}):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        for device in self.get_device_list():
            self.register_device(device, new=False)
        self.stimulus()
        self.measure()

    def set_device_data(self, device, index=0, sub_index=0):
        buf = self.error_model._buffers
        par = self.error_model._parameters
        if isinstance(device, NoLFZTuner):
            device._z_ = buf[rid2b(Response.Z_GET, index)][..., 0:1]
            device._z_set_ = buf[sid2b(Sweep.Z_SET, index)][..., 0:1]
        elif isinstance(device, NoRFZTuner):
            device._gamma_ = buf[rid2b(Response.G_GET, index)][..., 1::]
            device._gamma_set_ = buf[sid2b(Sweep.G_SET, index)][..., 1::]
        elif isinstance(device, NoLFReceiver):
            device._v_ = buf[rid2b(Response.V_GET, index)][..., 0:1]
            device._i_ = buf[rid2b(Response.I_GET, index)][..., 0:1]
            device._b_p_ = buf[rid2b(Response.B_GET, index)][..., 0:1]
            device._a_p_ = buf[rid2b(Response.A_GET, index)][..., 0:1]
        elif isinstance(device, NoRFReceiver):
            device._b_p_ = buf[rid2b(Response.B_GET, index)][..., 1::]
            device._a_p_ = buf[rid2b(Response.A_GET, index)][..., 1::]
            device._v_ = buf[rid2b(Response.V_GET, index)][..., 1::]
            device._i_ = buf[rid2b(Response.I_GET, index)][..., 1::]
        elif isinstance(device, NoLFSource):
            device._v_ = buf[sid2b(Sweep.V_SET, index)][..., 0:1]
        elif isinstance(device, NoRFSource):
            device._a_p_ = buf[sid2b(Sweep.A_SET, index)][..., 1::]
        elif isinstance(device, NoDUT):
            pass
        elif isinstance(device, NoMIPIServer):
            pass
        elif isinstance(device, NoMIPIClient):
            pass
        elif isinstance(device, NoVideo):
            device.video = par[rid2p(Response.VIDEO, index, sub_index)]
        elif isinstance(device, NoPM):
            device.p = par[rid2p(Response.P)]
        elif isinstance(device, NoSA):
            device.psd = par[rid2p(Response.PSD)]
        elif isinstance(device, NoVNA):
            device.sp = par[rid2p(Response.SP)]

    def set_all_device_data(self):
        for port_index, port in enumerate(self.ports):
            self.set_device_data(port.lfsource, port_index)
            self.set_device_data(port.lfreceiver, port_index)
            self.set_device_data(port.lfztuner, port_index)
            self.set_device_data(port.rfsource, port_index)
            self.set_device_data(port.rfreceiver, port_index)
            self.set_device_data(port.rfztuner, port_index)
        for dut_index, dut in enumerate(self.duts):
            self.set_device_data(dut, dut_index)
            for mipi_index, mipi in enumerate(dut.mipi):
                self.set_device_data(mipi, dut_index, mipi_index)
            for video_index, video in enumerate(dut.video):
                self.set_device_data(video, dut_index, video_index)

    def register_device(self, device, new=False):
        buf = self.error_model._buffers
        par = self.error_model._parameters
        if isinstance(device, NoLFZTuner):
            port_index = device.port
            if new:
                s = (self._sweep_step*Settings().t_points, 1)
                buf[rid2b(Response.Z_GET, port_index)][..., 0:1] = tf.delta(s, response_fill_map[Response.Z_GET])
                buf[sid2b(Sweep.Z_SET, port_index)][..., 0:1] = tf.delta(s, sweep_fill_map[Sweep.Z_SET])
            self.set_device_data(device, port_index)
            if port_index < len(self.ports):
                self.ports[port_index].lfztuner = device
        elif isinstance(device, NoRFZTuner):
            port_index = device.port
            if new:
                s = (self._sweep_step*Settings().t_points, Settings().f_points-1)
                buf[rid2b(Response.G_GET, port_index)][..., 1::] = tf.delta(s, response_fill_map[Response.G_GET])
                buf[sid2b(Sweep.G_SET, port_index)][..., 1::] = tf.delta(s, sweep_fill_map[Sweep.G_SET])
            self.set_device_data(device, port_index)
            if port_index < len(self.ports):
                self.ports[port_index].rfztuner = device
        elif isinstance(device, NoLFReceiver):
            port_index = device.port
            if new:
                buf[rid2b(Response.V_GET, port_index)][..., 0:1] = response_fill_map[Response.V_GET]
                buf[rid2b(Response.I_GET, port_index)][..., 0:1] = response_fill_map[Response.I_GET]
            self.set_device_data(device, port_index)
            if port_index < len(self.ports):
                self.ports[port_index].lfreceiver = device
        elif isinstance(device, NoRFReceiver):
            port_index = device.port
            if new:
                buf[rid2b(Response.B_GET, port_index)][..., 1::] = response_fill_map[Response.B_GET]
                buf[rid2b(Response.A_GET, port_index)][..., 1::] = response_fill_map[Response.A_GET]
            self.set_device_data(device, port_index)
            if port_index < len(self.ports):
                self.ports[port_index].rfreceiver = device
        elif isinstance(device, NoLFSource):
            port_index = device.port
            if new:
                buf[sid2b(Sweep.V_SET, port_index)][..., 0:1] = sweep_fill_map[Sweep.V_SET]
            self.set_device_data(device, port_index)
            if port_index < len(self.ports):
                self.ports[port_index].lfsource = device
        elif isinstance(device, NoRFSource):
            port_index = device.port
            if new:
                buf[sid2b(Sweep.A_SET, port_index)][..., 1::] = sweep_fill_map[Sweep.A_SET]
            self.set_device_data(device, port_index)
            if port_index < len(self.ports):
                self.ports[port_index].rfsource = device
        elif isinstance(device, NoDUT):
            dut_index = device.dut
            if new:
                pass
            self.set_device_data(device, dut_index)
            if dut_index < len(self.duts):
                self.duts[dut_index] = device
        elif isinstance(device, NoMIPIServer):
            dut_index = device.dut
            if new:
                pass
            self.set_device_data(device, dut_index)
            if dut_index < len(self.duts):
                self.duts[dut_index].mipi_server = device
        elif isinstance(device, NoMIPIClient):
            dut_index = device.dut
            mipi_index = device.index
            if new:
                pass
            self.set_device_data(device, dut_index, mipi_index)
            if dut_index < len(self.duts) and mipi_index < len(self.duts[dut_index].mipi):
                self.duts[dut_index].mipi[mipi_index] = device
        elif isinstance(device, NoVideo):
            dut_index = device.dut
            video_index = device.index
            if new:
                par[rid2p(Response.VIDEO, dut_index, video_index)].data[...] = response_fill_map[Response.VIDEO]
            self.set_device_data(device, dut_index, video_index)
            if dut_index < len(self.duts) and video_index < len(self.duts[dut_index].video):
                self.duts[dut_index].video[device.index] = device
        elif isinstance(device, NoPM):
            if new:
                par[rid2p(Response.P)].data[...] = response_fill_map[Response.P]
            self.set_device_data(device)
            self.aux[0] = device
        elif isinstance(device, NoSA):
            if new:
                par[rid2p(Response.PSD)].data[...] = response_fill_map[Response.PSD]
            self.set_device_data(device)
            self.aux[1] = device
        elif isinstance(device, NoVNA):
            if new:
                par[rid2p(Response.SP)].data[...] = response_fill_map[Response.SP]
            self.set_device_data(device)
            self.aux[2] = device

    def step(self):
        return self._step

    def sweep_step(self):
        return self._sweep_step

    def set_step(self, step):
        self._step = step
        self._sweep_step = step//Settings().t_points//Settings().f_points
        self.error_model = ErrorModel(len(self.ports) - 1, len(self.duts), len(self.duts[0].mipi), len(self.duts[0].video), self._sweep_step,
                                      old_model=self.error_model)
        self.set_all_device_data()

    def stimulus(self):
        """Convert from buffers to parameters"""
        buf = self.error_model._buffers
        viz_bag = [None] * len(self.ports)
        for ind, port in enumerate(self.ports):
            vb, ia, zg = buf[sid2b(Sweep.V_SET, ind)], buf[sid2b(Sweep.I_SET, ind)], buf[sid2b(Sweep.Z_SET, ind)]
            b, a, g = buf[sid2b(Sweep.B_SET, ind)], buf[sid2b(Sweep.A_SET, ind)], buf[sid2b(Sweep.G_SET, ind)]
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = b[..., 1:], a[..., 1:], g[..., 1:]
            vb, ia, zg = tf.ff(vb), tf.ff(ia), tf.ff(zg)
            zg[..., 1:] = g2z(zg[..., 1:])[0]
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = baz2viz(vb[..., 1:], ia[..., 1:], zg[..., 1:])
            viz_bag[ind] = [vb, ia, zg]

        for transform in self.transforms:
            viz_bag = transform.get_stimulus(*viz_bag)
        viz_bag = list(viz_bag)

        for ind, port in enumerate(self.ports):
            vb, ia, zg = viz_bag[ind]
            vb, ia, zg = ff.tf(vb), ff.tf(ia), ff.tf(zg)
            viz_bag[ind] = [vb, ia, zg]

        par = self.error_model._parameters
        for ind, port in enumerate(self.ports):
            vb, ia, zg = viz_bag[ind]
            vb, ia, zg = tf.ff(vb), tf.ff(ia), tf.ff(zg)
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = viz2baz(vb[..., 1:], ia[..., 1:], zg[..., 1:])
            zg[..., 1:] = z2g(zg[..., 1:])[0]
            vb, ia, zg = ff.tf(vb), ff.tf(ia), ff.tf(zg)
            par[sid2p(Sweep.Z_SET, ind)].data[...] = par[sid2p(Sweep.G_SET, ind)].data[...] = zg
            par[sid2p(Sweep.V_SET, ind)].data[...] = par[sid2p(Sweep.B_SET, ind)].data[...] = vb
            par[sid2p(Sweep.I_SET, ind)].data[...] = par[sid2p(Sweep.A_SET, ind)].data[...] = ia
            viz_bag[ind] = [vb, ia, zg]
        return viz_bag

    def set_stimulus(self, viz_bag=None):
        """Convert from parameters to buffers"""
        num_harmonics = Settings().num_harmonics
        par = self.error_model._parameters
        if viz_bag is None:
            viz_bag = [None]*len(self.ports)
        for ind, port in enumerate(self.ports):
            if viz_bag[ind] is None:
                vb, ia, zg = par[sid2p(Sweep.V_SET, ind)], par[sid2p(Sweep.I_SET, ind)], par[sid2p(Sweep.Z_SET, ind)]
                b, a, g = par[sid2p(Sweep.B_SET, ind)], par[sid2p(Sweep.A_SET, ind)], par[sid2p(Sweep.G_SET, ind)]
                with th.no_grad():
                    vb[..., 1:], ia[..., 1:], zg[..., 1:] = b[..., 1:], a[..., 1:], g[..., 1:]
            else:
                vb, ia, zg = viz_bag[ind]
                par[sid2p(Sweep.Z_SET, ind)].data[...] = par[sid2p(Sweep.G_SET, ind)].data[...] = zg
                par[sid2p(Sweep.V_SET, ind)].data[...] = par[sid2p(Sweep.B_SET, ind)].data[...] = vb
                par[sid2p(Sweep.I_SET, ind)].data[...] = par[sid2p(Sweep.A_SET, ind)].data[...] = ia
            vb, ia, zg = tf.ff(vb), tf.ff(ia), tf.ff(zg)
            zg[..., 1:] = g2z(zg[..., 1:])[0]
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = baz2viz(vb[..., 1:], ia[..., 1:], zg[..., 1:])
            viz_bag[ind] = [vb, ia, zg]

        for transform in reversed(self.transforms):
            viz_bag = transform.set_stimulus(*viz_bag)
        viz_bag = list(viz_bag)

        for ind, port in enumerate(self.ports):
            vb, ia, zg = viz_bag[ind]
            vb, ia, zg = ff.tf(vb), ff.tf(ia), ff.tf(zg)
            viz_bag[ind] = [vb, ia, zg]

        buf = self.error_model._buffers
        for ind, port in enumerate(self.ports):
            vb, ia, zg = viz_bag[ind]
            vb, ia, zg = tf.ff(vb), tf.ff(ia), tf.ff(zg)
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = viz2baz(vb[..., 1:], ia[..., 1:], zg[..., 1:])
            zg[..., 1:] = z2g(zg[..., 1:])[0]
            vb, ia, zg = ff.tf(vb), ff.tf(ia), ff.tf(zg)
            buf[sid2b(Sweep.Z_SET, ind)].data[...] = buf[sid2b(Sweep.G_SET, ind)].data[...] = zg
            buf[sid2b(Sweep.V_SET, ind)].data[...] = buf[sid2b(Sweep.B_SET, ind)].data[...] = vb
            buf[sid2b(Sweep.I_SET, ind)].data[...] = buf[sid2b(Sweep.A_SET, ind)].data[...] = ia
            port.lfztuner._z_set, port.rfztuner._gamma_set = zg.split([1, num_harmonics], -1)
            port.lfsource._v, _ = vb.split([1, num_harmonics], -1)
            _, port.rfsource._a_p = ia.split([1, num_harmonics], -1)

    def arm(self):
        for dut in self.duts:
            for mipi in dut.mipi:
                mipi.arm()
        for aux in self.aux:
            aux.arm()
        for port in self.ports:
            port.lfsource.arm(), port.lfreceiver.arm(), port.lfztuner.arm()
            port.rfsource.arm(), port.rfreceiver.arm(), port.rfztuner.arm()

    def trigger(self):
        trigger_device = Settings().trigger_device
        if trigger_device & DeviceFlag.INSTRUMENT:
            trigger_device = getattr(self.ports[Settings().trigger_port], device_name_map[trigger_device])
        elif trigger_device & DeviceFlag.DUT:
            trigger_device = self.duts[0]
        elif trigger_device & DeviceFlag.SUB_DUT:
            trigger_device = getattr(self.duts[0], device_name_map[trigger_device])
        trigger_device.trigger()

    # @line_profile(follow=[_es2fs, _fs2es])
    def measure(self):
        """Convert from buffers to parameters"""
        for port in self.ports:
            port.lfsource.measure(), port.lfreceiver.measure(), port.lfztuner.measure()
            port.rfsource.measure(), port.rfreceiver.measure(), port.rfztuner.measure()
        for aux in self.aux:
            aux.measure()
        for dut in self.duts:
            for mipi in dut.mipi:
                mipi.measure()

        buf = self.error_model._buffers
        num_harmonics = Settings().num_harmonics
        viz_bag = [None] * len(self.ports)
        for ind, port in enumerate(self.ports):
            vb, ia, zg = buf[rid2b(Response.V_GET, ind)], buf[rid2b(Response.I_GET, ind)], buf[rid2b(Response.Z_GET, ind)]
            b, a, g = buf[rid2b(Response.B_GET, ind)], buf[rid2b(Response.A_GET, ind)], buf[rid2b(Response.G_GET, ind)]
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = b[..., 1:], a[..., 1:], g[..., 1:]
            vb, ia, zg = tf.ff(vb), tf.ff(ia), tf.ff(zg)
            zg[..., 1:] = g2z(zg[..., 1:])[0]
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = baz2viz(vb[..., 1:], ia[..., 1:], zg[..., 1:])
            viz_bag[ind] = [vb, ia, zg]

        for transform in self.transforms:
            viz_bag = transform.get_response(*viz_bag)
        viz_bag = list(viz_bag)

        for ind, port in enumerate(self.ports):
            vb, ia, zg = viz_bag[ind]
            vb, ia, zg = ff.tf(vb), ff.tf(ia), ff.tf(zg)
            viz_bag[ind] = [vb, ia, zg]

        par = self.error_model._parameters
        for ind, port in enumerate(self.ports):
            vb, ia, zg = viz_bag[ind]
            vb, ia, zg = tf.ff(vb), tf.ff(ia), tf.ff(zg)
            vb[..., 1:], ia[..., 1:], zg[..., 1:] = viz2baz(vb[..., 1:], ia[..., 1:], zg[..., 1:])
            zg[..., 1:] = z2g(zg[..., 1:])[0]
            vb, ia, zg = ff.tf(vb), ff.tf(ia), ff.tf(zg)
            par[rid2p(Response.Z_GET, ind)].data[...] = par[rid2p(Response.G_GET, ind)].data[...] = zg
            par[rid2p(Response.V_GET, ind)].data[...] = par[rid2p(Response.B_GET, ind)].data[...] = vb
            par[rid2p(Response.I_GET, ind)].data[...] = par[rid2p(Response.A_GET, ind)].data[...] = ia
            viz_bag[ind] = [vb, ia, zg]

        aux = [par[rid2p(Response.SS_FREQ)], par[rid2p(Response.P)], par[rid2p(Response.PSD)], par[rid2p(Response.SP)]]
        return viz_bag, aux

    def moveToThread(self, thread):
        """
        Changes the thread affinity (lifetime) for self and its children.

        When thread is deleted, self is deleted. Marshals an interface pointer from one thread to another thread in
        the same process.
        """
        if sys.platform == "win32": pythoncom.CoInitialize()
        for device in self.get_device_list():
            for k, v in device.handles.items():
                if hasattr(v, "coclass_clsid") and hasattr(device, "machine_name"):
                    key = (id(device), k, device.machine_name)
                    com = device.handles[key[-2]]
                    com_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, com)
                    self._marshall_map[key] = com_id

    def runInThread(self, thread):
        """
        Changes the thread that is run for self and its children.

        When a method of self is executed, this thread becomes active(blocking). Each method should call self.exec_()
        when it is finished so that the thread can return to its event loop. Unmarshals a buffer containing an interface
        pointer and releases the stream when an interface pointer has been marshaled from another thread to the calling
        thread.
        """
        if sys.platform == "win32": pythoncom.CoInitialize()
        for device in self.get_device_list():
            for k, v in device.handles.items():
                if hasattr(v, "coclass_clsid") and hasattr(device, "machine_name"):
                    key = (id(device), k, device.machine_name)
                    com_id = self._marshall_map[key]
                    clsid = pythoncom.CoGetInterfaceAndReleaseStream(com_id, pythoncom.IID_IDispatch)
                    device.handles[k] = Dispatch(clsid, key[-1])

    def get_device_list(self):
        devices = []
        for port in self.ports:
            devices += [port.lfsource, port.lfreceiver, port.lfztuner, port.rfsource, port.rfreceiver, port.rfztuner]
        devices += self.aux
        devices += self.duts
        return devices

    def disconnect_handles(self):
        for device in self.get_device_list():
            device.disconnect_handles()

    def _add_handle_ref(self, handle):
        key = DevicesModel._handle2key(handle)
        if key not in self._handle_ref_map:
            self._handle_ref_map[key] = 1
        else:
            self._handle_ref_map[key] += 1

    def _remove_handle_ref(self, handle):
        key = DevicesModel._handle2key(handle)
        self._handle_ref_map[key] -= 1
        if self._handle_ref_map[key] == 0:
            self._handle_ref_map.pop(key)
            if isinstance(handle, Resource):
                handle.clear()
                handle.close()

    def _handle_ref_count(self, handle):
        key = DevicesModel._handle2key(handle)
        return self._handle_ref_map[key]

    @staticmethod
    def _handle2key(handle):
        if isinstance(handle, AbstractSimulator):  # Simulator
            key = handle.__class__.__name__
        elif isinstance(handle, Resource):  # VISA
            key = handle.resource_info
        elif hasattr(handle, "coclass_clsid"):  # COM
            key = handle.coclass_clsid
        elif isinstance(handle, object) and hasattr(handle, "id"):  # PyObject
            key = handle.id
        else:
            raise TypeError("Unsupported Instrument Handle")
        return key


