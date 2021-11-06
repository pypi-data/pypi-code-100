import os
from collections import OrderedDict

import torch as th
import tables as tb

from sknrf.enums.runtime import SI, si_dtype_map
from sknrf.enums.device import Response, rid2p
from sknrf.enums.sequencer import Sweep, required_sweeps, sid2p, p2sid
from sknrf.enums.sequencer import sweep_name_map
from sknrf.enums.sequencer import sweep_dtype_map, sweep_device_map
from sknrf.settings import Settings
from sknrf.device.signal import tf
from sknrf.app.dataviewer.model import DatagroupModel
from sknrf.model.runtime import RuntimeModel
from sknrf.model.sequencer.sweep.complex import CustomSweep
from sknrf.model.sequencer.sweep.frequency import FundDSBSpanSweep, FundSSBSpanSweep, FundPhasorSpanSweep, FundLOSpanSweep
from sknrf.utilities.numeric import Info
from sknrf.utilities.patterns import export, export_runtime
from sknrf.utilities.rf import viz2baz
from sknrf.utilities.dsp import iq_delay, iq_phase, fund_dsb, fund_ssb, fund_phasor, ind_grid, fm_grid


class Measure(RuntimeModel):

    display_order = []

    def __new__(cls, ports=tuple(), duts=tuple(), mipis=tuple(), videos=tuple(), ss_ports=tuple()):
        self = super(Measure, cls).__new__(cls)
        self.ports = list(range(Settings().num_ports + 1)) if len(ports) == 0 else ports
        self.duts = list(range(Settings().num_duts + 1)) if len(duts) == 0 else duts
        self.mipis = list(range(Settings().num_mipi + 1)) if len(mipis) == 0 else mipis
        self.videos = list(range(Settings().num_video + 1)) if len(videos) == 0 else videos
        self.ss_ports = list(range(Settings().num_ports + 1)) if len(ss_ports) == 0 else ss_ports
        self._sweep_plan_map = OrderedDict()
        self._clear_sweeps()
        return self

    def __getnewargs__(self):
        return self.ports, self.duts, self.mipis, self.videos, self.ss_ports

    @export
    def __init__(self, ports=tuple(), duts=tuple(), mipis=tuple(), videos=tuple(), ss_ports=tuple()):
        super(Measure, self).__init__()
        self.ports = list(range(Settings().num_ports + 1)) if len(ports) == 0 else ports
        self.duts = list(range(Settings().num_duts + 1)) if len(duts) == 0 else duts
        self.mipis = list(range(Settings().num_mipi + 1)) if len(mipis) == 0 else mipis
        self.videos = list(range(Settings().num_video + 1)) if len(videos) == 0 else videos
        self.ss_ports = list(range(Settings().num_ports + 1)) if len(ss_ports) == 0 else ss_ports
        self._sweep_plan_map = OrderedDict()
        self._clear_sweeps()
        self.__info__()

    def __getstate__(self, state={}):
        state = super(Measure, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(Measure, self).__setstate__(state)
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###

    def __info__(self):
        super(Measure, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["ports"] = Info("ports", read=True, write=True, check=True)
        self.info["duts"] = Info("duts", read=True, write=True, check=True)
        self.info["mipis"] = Info("mipis", read=True, write=True, check=True)
        self.info["videos"] = Info("videos", read=True, write=True, check=True)
        self.info["ss_ports"] = Info("ss_ports", read=True, write=True, check=True)

    @export
    def add_sweep(self, sweep_id, port_index=None, harm_index=None, sweep_plan=None):
        if isinstance(sweep_id, str):
            sweep_id = Sweep[sweep_id.upper()]
        elif sweep_plan is None:
            sweep_id = CustomSweep(realtime=False, values=[0.0])
        self._sweep_plan_map[sid2p(sweep_id, port_index, harm_index)] = sweep_plan

    @export
    def remove_sweep(self, sweep_id, port_index=None, harm_index=None):
        self._sweep_plan_map.pop(sid2p(sweep_id, port_index, harm_index))

    def _clear_sweeps(self):
        self._sweep_plan_map.clear()
        sweep_values = th.as_tensor(Settings().freq,
                                    dtype=sweep_dtype_map[Sweep.FREQ], device=sweep_device_map[Sweep.FREQ])
        self.add_sweep(Sweep.FREQ, sweep_plan=CustomSweep(True, sweep_values))
        sweep_values = th.as_tensor(Settings().time,
                                    dtype=sweep_dtype_map[Sweep.TIME], device=sweep_device_map[Sweep.TIME])
        self.add_sweep(Sweep.TIME, sweep_plan=CustomSweep(True, sweep_values))

    def _replace_sweep(self, sweep_names, sweep_plans, sweep_plan, sweep_id, port_index=None, harm_index=None):
        replace_name = sid2p(sweep_id, port_index=port_index, harm_index=harm_index)
        try:
            replace_index = sweep_names.index(replace_name)
        except ValueError:
            pass
        else:
            sweep_plans[replace_index] = sweep_plan

    def _required_preprocessor(self, sweep_plan_map):
        ports = self.device_model().ports
        for sweep_id in required_sweeps:
            sweep_name = sid2p(sweep_id)
            if sweep_id & Sweep.FREQ and sweep_name not in sweep_plan_map:
                sweep_values = th.as_tensor(Settings().freq)
                sweep_plan_map[sweep_name] = CustomSweep(True, sweep_values)
                continue
            elif sweep_id & Sweep.TIME and sweep_name not in sweep_plan_map:
                sweep_values = th.as_tensor(Settings().time)
                sweep_plan_map[sweep_name] = CustomSweep(True, sweep_values)
                continue
            for port_index in self.ports:
                for harm_index in range(0, Settings().f_points):
                    sweep_name = sid2p(sweep_id, port_index, harm_index)
                    if sweep_id & Sweep.A_SET and sweep_name not in sweep_plan_map and harm_index > 0:
                        sweep_values = ports[port_index].rfsource.a_p[:, harm_index-1:harm_index].unsqueeze(0)
                        sweep_plan_map[sweep_name] = CustomSweep(False, sweep_values)
                    elif sweep_id & Sweep.V_SET and sweep_name not in sweep_plan_map and harm_index < 1:
                        sweep_values = ports[port_index].lfsource.v[:, harm_index:harm_index+1].unsqueeze(0)
                        sweep_plan_map[sweep_name] = CustomSweep(False, sweep_values)
                    elif sweep_id & Sweep.Z_SET and sweep_name not in sweep_plan_map and harm_index < 1:
                        sweep_values = ports[port_index].lfztuner.z_set[:, harm_index:harm_index+1].unsqueeze(0)
                        sweep_plan_map[sweep_name] = CustomSweep(False, sweep_values)
                    elif sweep_id & Sweep.G_SET and sweep_name not in sweep_plan_map and harm_index > 0:
                        sweep_values = ports[port_index].rfztuner.gamma_set[:, harm_index-1:harm_index].unsqueeze(0)
                        sweep_plan_map[sweep_name] = CustomSweep(False, sweep_values)
                    elif sweep_id & Sweep.LO and sweep_name not in sweep_plan_map:
                        sweep_values = th.as_tensor(ports[port_index].rfsource.f0)
                        sweep_plan_map[sweep_name] = CustomSweep(False, sweep_values)
        return sweep_plan_map

    def _replacement_preprocessor(self, sweep_plan_map):
        ports = self.device_model().ports
        sweep_names = list(sweep_plan_map.keys())
        sweep_plans = list(sweep_plan_map.values())
        new_sweep_plan_map = OrderedDict()
        sweep_index, num_sweeps = 0, len(sweep_names)
        while sweep_index < num_sweeps:
            sweep_name, sweep_plan = sweep_names[sweep_index], sweep_plans[sweep_index]
            sweep_id, port_index, harm_index = p2sid(sweep_name)
            if sweep_id & Sweep.PHASE:
                signal = th.cat((ports[port_index].lfsource.v, ports[port_index].rfsource.a_p), dim=-1)
                sweep_values = iq_phase(signal, sweep_plan.values())
                harm_range = range(0, Settings().f_points+1) if harm_index < 0 else range(harm_index, harm_index+1)
                for harm_index in harm_range:
                    sweep_plan = CustomSweep(sweep_plan.realtime, sweep_values[:, :, harm_index:harm_index+1])
                    self._replace_sweep(sweep_names, sweep_plans, sweep_plan, Sweep.V_SET, port_index, harm_index)
                    self._replace_sweep(sweep_names, sweep_plans, sweep_plan, Sweep.A_SET, port_index, harm_index)
                del sweep_names[sweep_index], sweep_plans[sweep_index]
                num_sweeps -= 1
                continue
            elif sweep_id & Sweep.TAU:
                signal = th.cat((ports[port_index].lfsource.v, ports[port_index].rfsource.a_p), dim=-1)
                sweep_values = iq_delay(signal, sweep_plan.values())
                harm_range = range(0, Settings().f_points+1) if harm_index < 0 else range(harm_index, harm_index+1)
                for harm_index in harm_range:
                    sweep_plan = CustomSweep(sweep_plan.realtime, sweep_values[:, :, harm_index:harm_index+1])
                    self._replace_sweep(sweep_names, sweep_plans, sweep_plan, Sweep.V_SET, port_index, harm_index)
                    self._replace_sweep(sweep_names, sweep_plans, sweep_plan, Sweep.A_SET, port_index, harm_index)
                del sweep_names[sweep_index], sweep_plans[sweep_index]
                num_sweeps -= 1
                continue
            elif sweep_id & Sweep.SP_FUND:
                iq_data = tf.iq(ports[port_index].rfsource.a_p)
                sweep_name = sweep_name_map[Sweep.SP_FUND]
                if Settings().ss_mod == "dsb":
                    sweep_values = fund_dsb(iq_data, sweep_plan.values(), sweep_plan.level, sweep_plan.all)
                elif Settings().ss_mod == "ssb":
                    sweep_values = fund_ssb(iq_data, sweep_plan.values(), sweep_plan.level, sweep_plan.all)
                elif Settings().ss_mod == "phasor":
                    sweep_values = fund_phasor(iq_data, sweep_plan.values(), sweep_plan.level, sweep_plan.all)
                else:
                    sweep_values = sweep_plan.values()
                sweep_plan = CustomSweep(sweep_plan.realtime, sweep_values)
            sweep_index += 1
            new_sweep_plan_map[sweep_name] = sweep_plan
        return new_sweep_plan_map

    def _sp_preprocessor(self, sweep_plan_map):
        sweep_names = list(sweep_plan_map.keys())
        sweep_plans = list(sweep_plan_map.values())
        new_sweep_plan_map = OrderedDict()
        sweep_index, num_sweeps = 0, len(sweep_plan_map)
        while sweep_index < num_sweeps:
            sweep_name, sweep_plan = sweep_names[sweep_index], sweep_plans[sweep_index]
            sweep_id, port_index, harm_index = p2sid(sweep_name)
            if sweep_id & Sweep.SP_PORT:
                sp_fund = sweep_plan_map[sid2p(Sweep.SP_FUND)].values()
                sp_harm = sweep_plan_map[sid2p(Sweep.SP_HARM)].values().reshape(1,  -1,  1, 1, 1)
                sp_port = sweep_plan_map[sid2p(Sweep.SP_PORT)].values().reshape(-1,  1,  1, 1, 1)
                for port_index, port_num in enumerate(sweep_plan.values().detach().numpy()):
                    port_mask = th.zeros_like(sp_port, dtype=sp_fund.dtype)
                    port_mask[port_index, ...] = 1.0
                    for harm_index, harm_num in enumerate(sp_harm.reshape(-1).tolist()):
                        harm_mask = th.zeros_like(sp_harm, dtype=sp_fund.dtype)
                        harm_mask[:, harm_index, ...] = 1.0
                        new_sweep_values = (port_mask*harm_mask*sp_fund).unsqueeze(0)*Settings().ss_power
                        new_sweep_plan = CustomSweep(sweep_plan.realtime, new_sweep_values)
                        self._replace_sweep(sweep_names, sweep_plans, new_sweep_plan, Sweep.V_SET, port_num, harm_num)
                        self._replace_sweep(sweep_names, sweep_plans, new_sweep_plan, Sweep.A_SET, port_num, harm_num)
            sweep_index += 1
            new_sweep_plan_map[sweep_name] = sweep_plan
        return new_sweep_plan_map

    def _iteration_preprocessor(self, sweep_plan_map):
        if Settings().sweep_avg > 1:  # Averaging
            sweep_name = sweep_name_map[Sweep.AVG]
            sweep_values = th.range(0, Settings().sweep_avg,
                                    dtype=sweep_dtype_map[Sweep.AVG], device=sweep_device_map[Sweep.AVG])
            sweep_plan_map[sweep_name] = CustomSweep(realtime=False, values=sweep_values)
        if Settings().sweep_rep > 1:  # Repetitions
            sweep_name = sweep_name_map[Sweep.REP]
            sweep_values = th.range(0, Settings().sweep_rep,
                                    dtype=sweep_dtype_map[Sweep.REP], device=sweep_device_map[Sweep.REP])
            sweep_plan_map[sweep_name] = CustomSweep(realtime=False, values=sweep_values)
        return sweep_plan_map

    def _cleanup_preprocessor(self, sweep_plan_map):
        ports = self.device_model().ports
        sweep_names = list(sweep_plan_map.keys())
        sweep_plans = list(sweep_plan_map.values())
        sweep_index, num_sweeps = 0, len(sweep_names)
        while sweep_index < num_sweeps:
            sweep_name, sweep_plan = sweep_names[sweep_index], sweep_plans[sweep_index]
            realtime = sweep_plan_map[sweep_name].realtime
            sweep_id, port_index, harm_index = p2sid(sweep_name)
            if sweep_id & Sweep.PHASE:
                old_shape = sweep_plan.values().shape
                new_shape = [1]*len(old_shape)
                new_shape[0] = old_shape[0]
                sweep_values = self._sweep_plan_map[sweep_name].values().reshape(new_shape)
                sweep_plan_map[sweep_name] = CustomSweep(realtime, sweep_values)
            elif sweep_id & Sweep.TAU:
                old_shape = sweep_plan.values().shape
                new_shape = [1]*len(old_shape)
                new_shape[0] = old_shape[0]
                sweep_values = self._sweep_plan_map[sweep_name].values().reshape(new_shape)
                sweep_plan_map[sweep_name] = CustomSweep(realtime, sweep_values)
            elif sweep_id & Sweep.SP_FUND:
                old_shape = sweep_plan.values().shape
                new_shape = [1]*len(old_shape)
                new_shape[0] = old_shape[0]
                sweep_values = self._sweep_plan_map[sweep_name].values().reshape(new_shape)
                sweep_plan_map[sweep_name] = CustomSweep(realtime, sweep_values)
            elif sweep_id & Sweep.SP_HARM:
                old_shape = sweep_plan.values().shape
                new_shape = [1]*len(old_shape)
                new_shape[0] = old_shape[0]
                sweep_values = self._sweep_plan_map[sweep_name].values().reshape(new_shape)
                sweep_plan_map[sweep_name] = CustomSweep(realtime, sweep_values)
            elif sweep_id & Sweep.SP_PORT:
                old_shape = sweep_plan.values().shape
                new_shape = [1]*len(old_shape)
                new_shape[0] = old_shape[0]
                sweep_values = self._sweep_plan_map[sweep_name].values().reshape(new_shape)
                sweep_plan_map[sweep_name] = CustomSweep(realtime, sweep_values)
            sweep_index += 1
        return sweep_plan_map

    def create_indep_map(self):
        indep_map = OrderedDict((
            ("freq_m", Settings().freq_m),
            ("time_c", Settings().time_c)
        ))
        return indep_map

    def create_sweep_map(self):
        ports = self.device_model().ports
        sweep_plan_map = self._sweep_plan_map.copy()
        sweep_plan_map = self._required_preprocessor(sweep_plan_map)
        sweep_plan_map = self._replacement_preprocessor(sweep_plan_map)
        sweep_plan_map = self._sp_preprocessor(sweep_plan_map)
        sweep_plan_map = self._iteration_preprocessor(sweep_plan_map)
        sweep_plan_map = self._cleanup_preprocessor(sweep_plan_map)

        # Convert sweep_plan_map to sweep_map
        sweep_map = OrderedDict()
        step = 1
        for sweep_index, (sweep_name, sweep_plan) in enumerate(sweep_plan_map.items()):
            sweep_id, port_index, harm_index = p2sid(sweep_name)
            sweep_values = sweep_plan.values()
            if sweep_values.dim() == 1:
                if sweep_id & Sweep.A_SET:
                    iq = tf.iq(ports[port_index].rfsource.a_p)
                    fill_ = th.zeros((Settings().t_points, Settings().f_points), dtype=iq.dtype)
                    sweep_values = sweep_values.reshape(-1, 1, 1) * iq + fill_
                elif sweep_id & Sweep.V_SET:
                    iq = tf.iq(ports[port_index].lfsource.v)
                    fill_ = th.zeros((Settings().t_points, Settings().f_points), dtype=iq.dtype)
                    sweep_values = sweep_values.reshape(-1, 1, 1) * iq + fill_
                elif sweep_id & Sweep.Z_SET:
                    iq = tf.iq(ports[port_index].lfztuner.z_set)
                    fill_ = th.zeros((Settings().t_points, Settings().f_points), dtype=iq.dtype)
                    sweep_values = sweep_values.reshape(-1, 1, 1) * iq + fill_
                elif sweep_id & Sweep.G_SET:
                    iq = tf.iq(ports[port_index].rfztuner.gamma_set)
                    fill_ = th.zeros((Settings().t_points, Settings().f_points), dtype=iq.dtype)
                    sweep_values = sweep_values.reshape(-1, 1, 1) * iq + fill_
            step *= sweep_values.shape[0] if sweep_plan.realtime else 1
            sweep_shape = list(sweep_values.shape)
            while len(sweep_shape) < sweep_index+1:
                sweep_shape.insert(1, 1)
            while len(sweep_shape) < len(sweep_plan_map):
                sweep_shape.insert(0, 1)
            sweep_values = sweep_values.reshape(sweep_shape)
            sweep_map[sweep_name] = sweep_values
        return sweep_map, step

    # @c_profile(filename=os.sep.join((Settings().root, "..", "benchmarking", "swept_measurement.pstat")))
    @export_runtime
    def swept_measurement(self, *args, **kwargs):
        sweep_map, step = self.create_sweep_map()
        indep_map = self.create_indep_map()
        self.runInThread(self.thread())
        loss = 0.0
        self.threshold = -1.0

        # Initialize Device Model
        initial_stimulus = self.device_model().stimulus()
        self.device_model().set_step(step)

        # Initialize Dataset Model
        self._add_datagroup(Settings().datagroup)
        dg = self.datagroup_model()[Settings().datagroup]
        if dg.has_dataset(Settings().dataset):
            dg.remove(Settings().dataset)
        ds = dg.add(Settings().dataset, self.ports, self.duts, self.videos,
                    sweep_map=sweep_map, indep_map=indep_map)
        di = ds.__iter__(step)

        self.start()  # Open Runtime
        try:
            for batch_index, viz_bag in di:
                # while loss > self.threshold:
                self.check_state()

                self.device_model().set_stimulus(viz_bag)  # Apply Stimulus
                self.device_model().arm()
                self.device_model().trigger()
                viz_bag, aux = self.device_model().measure()

                # loss = self.loss_func(response_map, goal_map)
                # loss.backward()
                # self.opt.step()
                # self.opt.zero_grad()
                di.save(viz_bag, aux)
                self.update(batch_index)  # Update Runtime
                self.threshold = 1.0
        except InterruptedError:
            pass
        finally:
            self.device_model().set_step(Settings().t_points*Settings().f_points)
            self.device_model().set_stimulus(initial_stimulus)
            self.datagroup_model()[Settings().datagroup].flush()
            self.stop()

    @export_runtime
    def skip_measurement(self, *args, **kwargs):
        pass

    # @c_profile(filename=os.sep.join((Settings().root, "..", "benchmarking", "single_measurement.pstat")))
    # @export
    def single_measurement(self, *args, **kwargs):
        Settings().datagroup = "Single"
        Settings().dataset = "Single"
        dg_name, ds_name = Settings().datagroup, Settings().dataset
        sweep_plan_map = self._sweep_plan_map.copy()
        self._clear_sweeps()
        try:
            self.swept_measurement()
        finally:
            pass
            # self._sweep_plan_map = sweep_plan_map
            # Settings().datagroup = dg_name
            # Settings().datagroup = ds_name

    def compute_sparameters(self, ds):
        ports = self.ss_ports
        num_fund = Settings().ss_points
        s_shape = th.prod(th.as_tensor(ds.shape[-4:-2])), ds.shape[-5], ds.shape[-5]
        s = th.empty(s_shape, dtype=si_dtype_map[SI.B])
        b, a, = [None] * len(ports), [None] * len(ports)
        for port_index, port_num in enumerate(ports):
            ia = tf.ff(getattr(ds, rid2p(Response.A_GET, port_num))[...])
            vb = tf.ff(getattr(ds, rid2p(Response.B_GET, port_num))[...])
            if Settings().ss_ref == "stimulus":
                vb[..., 0] = tf.ff(getattr(ds, sid2p(Sweep.V_SET, port_num, 0))[...])[..., 0]
                for harm_index in range(Settings().f_points - 1):
                    harm_num = harm_index + 1
                    ia[..., harm_num] += tf.ff(getattr(ds, sid2p(Sweep.A_SET, port_num, harm_num))[...])[
                        ..., harm_num]
            else:
                vb[..., 0] = tf.ff(getattr(ds, rid2p(Response.V_GET, port_num))[...])[..., 0]
                ia[..., 1:] = tf.ff(getattr(ds, rid2p(Response.A_GET, port_num))[...])[..., 1:]
            vb[..., 0:1], ia[..., 0:1], _ = viz2baz(vb[..., 0:1], ia[..., 0:1])
            b[port_index], a[port_index] = vb, ia

        ds_shape = [1] * len(ds.shape)
        ds_shape[-4], ds_shape[-3] = ds.shape[-4], 1
        ds_index = th.arange(0, ds.shape[-4], 1, dtype=th.int64).reshape(ds_shape)
        harm_values = ds.sp_harm[...].gather(-4, ds_index).flatten()
        ds_shape[-4], ds_shape[-3] = 1, ds.shape[-3]
        ds_index = th.arange(0, ds.shape[-3], 1, dtype=th.int64).reshape(ds_shape)
        fm = fm_grid(ds.sp_fund[...].gather(-3, ds_index))
        fund_indices = th.linspace(0, num_fund - 1, num_fund, dtype=th.int64)
        sp_time_indices = ind_grid(fm)[fund_indices].flatten()
        for src_index in range(len(ports)):
            for rcvr_index in range(len(ports)):
                for harm_index, harm_num in enumerate(harm_values):
                    harm_offset = num_fund * harm_index
                    _b = b[rcvr_index][..., src_index, harm_index, fund_indices, sp_time_indices, harm_num]
                    _a = a[src_index][..., src_index, harm_index, fund_indices, sp_time_indices, harm_num]
                    _s = (_b / _a).flatten()
                    s[harm_offset + fund_indices, rcvr_index, src_index] = _s
        ds.s[...] = s.detach()

    # @c_profile(filename="../benchmarking/single_measurement.pstat")
    @export_runtime
    def single_sparameter_measurement(self, *args, **kwargs):
        dg_name, ds_name = Settings().datagroup, Settings().dataset
        sweep_plan_map = self._sweep_plan_map.copy()
        ss_realtime = Settings().ss_realtime
        self._clear_sweeps()
        if Settings().ss_mod == "dsb":
            self.add_sweep(Sweep.SP_FUND, sweep_plan=FundDSBSpanSweep(ss_realtime))
        elif Settings().ss_mod == "ssb":
            self.add_sweep(Sweep.SP_FUND, sweep_plan=FundSSBSpanSweep(ss_realtime))
        elif Settings().ss_mod == "phasor":
            self.add_sweep(Sweep.SP_FUND, sweep_plan=FundPhasorSpanSweep(ss_realtime))
        else:
            self.add_sweep(Sweep.SP_FUND, sweep_plan=FundLOSpanSweep(ss_realtime))
        if Settings().ss_harm == "lf":
            harm_start, harm_stop = 0, 1
        elif Settings().ss_harm == "rf":
            harm_start, harm_stop = 1, Settings().f_points
        else:
            harm_start, harm_stop = 0, Settings().f_points
        sweep_values = th.arange(harm_start, harm_stop,
                                 dtype=sweep_dtype_map[Sweep.SP_HARM], device=sweep_device_map[Sweep.SP_HARM])
        self.add_sweep(Sweep.SP_HARM, sweep_plan=CustomSweep(ss_realtime, sweep_values))
        sweep_values = th.as_tensor(self.ss_ports,
                                    dtype=sweep_dtype_map[Sweep.SP_PORT], device=sweep_device_map[Sweep.SP_PORT])
        self.add_sweep(Sweep.SP_PORT, sweep_plan=CustomSweep(ss_realtime, sweep_values))
        try:
            self.swept_measurement()
            dg = self.datagroup_model()[Settings().datagroup]
            ds = dg.dataset(Settings().dataset)
        finally:
            self._sweep_plan_map = sweep_plan_map
            Settings().datagroup = dg_name
            Settings().dataset = ds_name
        self.compute_sparameters(ds)

    def _add_datagroup(self, dg_name):
        dg_model = self.datagroup_model()
        dg_name = Settings().datagroup
        try:
            dg_filename = dg_model[dg_name].filename
            dg_model[dg_name].close()
        except KeyError:
            dg_filename = os.sep.join((Settings().data_root, "datagroups", dg_name + ".h5"))
        dg_model[dg_name] = DatagroupModel(dg_filename, mode="a")
