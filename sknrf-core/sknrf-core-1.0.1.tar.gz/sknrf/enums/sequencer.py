from enum import Flag, auto, unique

import torch as th

from sknrf.settings import Settings
from sknrf.enums.runtime import SI, si_dtype_map, si_eps_map


class Sweep(Flag):
    FREQ = auto()
    TIME = auto()
    FREQ_M = auto()
    TIME_C = auto()
    TAU = auto()
    PHASE = auto()
    V_SET = auto()
    I_SET = auto()
    Z_SET = auto()
    B_SET = auto()
    A_SET = auto()
    G_SET = auto()
    LO = auto()
    SP_FUND = auto()
    SP_HARM = auto()
    SP_PORT = auto()
    SP_POWER = auto()
    TEMP = auto()
    AVG = auto()
    REP = auto()
    VIZ = V_SET | I_SET | Z_SET
    BAG = B_SET | A_SET | G_SET
    LS = TIME | FREQ | FREQ_M | TIME_C | VIZ | BAG
    SP = SP_FUND | SP_HARM | SP_PORT | SP_POWER
    DUT = TEMP


required_sweeps = [Sweep.FREQ, Sweep.TIME, Sweep.A_SET, Sweep.V_SET, Sweep.Z_SET, Sweep.G_SET]


sweep_name_map = {
    Sweep.FREQ:        "freq",
    Sweep.TIME:        "time",
    Sweep.FREQ_M:      "freq_m",
    Sweep.TIME_C:      "time_c",
    Sweep.TAU:         "tau",
    Sweep.PHASE:       "phase",
    Sweep.V_SET:       "v_set",
    Sweep.I_SET:       "i_set",
    Sweep.Z_SET:       "z_set",
    Sweep.B_SET:       "b_set",
    Sweep.A_SET:       "a_set",
    Sweep.G_SET:       "g_set",
    Sweep.LO:          "lo",
    Sweep.SP_FUND:     "sp_fund",
    Sweep.SP_HARM:     "sp_harm",
    Sweep.SP_PORT:     "sp_port",
    Sweep.SP_POWER:    "sp_power",
    Sweep.TEMP:        "temp_c",
    Sweep.AVG:         "avg",
    Sweep.REP:         "rep",
}

name_sweep_map = dict(zip(sweep_name_map.values(), sweep_name_map.keys()))


sweep_shape_map = {
    Sweep.FREQ:         (1,                   Settings().f_points),
    Sweep.TIME:         (Settings().t_points, 1),
    Sweep.FREQ_M:       (Settings().t_points, 1),
    Sweep.TIME_C:       (1,                   Settings().f_points),
    Sweep.TAU:          (1,                   1),
    Sweep.PHASE:        (1,                   1),
    Sweep.V_SET:        (Settings().t_points, Settings().f_points),
    Sweep.I_SET:        (Settings().t_points, Settings().f_points),
    Sweep.Z_SET:        (Settings().t_points, Settings().f_points),
    Sweep.B_SET:        (Settings().t_points, Settings().f_points),
    Sweep.A_SET:        (Settings().t_points, Settings().f_points),
    Sweep.G_SET:        (Settings().t_points, Settings().f_points),
    Sweep.LO:           (1,                   1),
    Sweep.SP_FUND:      (1,                   1),
    Sweep.SP_HARM:      (1,                   1),
    Sweep.SP_PORT:      (1,                   1),
    Sweep.SP_POWER:     (1,                   1),
    Sweep.TEMP:         (Settings().t_points, 1),
    Sweep.AVG:          (1, 1),
    Sweep.REP:          (1, 1),
}

sweep_dtype_map = {
    Sweep.FREQ:         si_dtype_map[SI.F],
    Sweep.TIME:         si_dtype_map[SI.T],
    Sweep.FREQ_M:       si_dtype_map[SI.F],
    Sweep.TIME_C:       si_dtype_map[SI.T],
    Sweep.TAU:          si_dtype_map[SI.T],
    Sweep.PHASE:        th.double,
    Sweep.V_SET:        si_dtype_map[SI.V],
    Sweep.I_SET:        si_dtype_map[SI.I],
    Sweep.Z_SET:        si_dtype_map[SI.Z],
    Sweep.B_SET:        si_dtype_map[SI.B],
    Sweep.A_SET:        si_dtype_map[SI.A],
    Sweep.G_SET:        si_dtype_map[SI.G],
    Sweep.LO:           si_dtype_map[SI.F],
    Sweep.SP_FUND:      si_dtype_map[SI.F],
    Sweep.SP_HARM:      th.short,
    Sweep.SP_PORT:      th.short,
    Sweep.SP_POWER:     si_dtype_map[SI.A],
    Sweep.TEMP:         si_dtype_map[SI.TEMP],
    Sweep.AVG:          th.short,
    Sweep.REP:          th.short,
}

sweep_fill_map = {
    Sweep.FREQ:         Settings().f0,
    Sweep.TIME:         Settings().t_step,
    Sweep.FREQ_M:       Settings().f0,
    Sweep.TIME_C:       1/Settings().f0,
    Sweep.TAU:          Settings().t_step,
    Sweep.PHASE:        0.0,
    Sweep.V_SET:        si_eps_map[SI.V],
    Sweep.I_SET:        si_eps_map[SI.I],
    Sweep.Z_SET:        si_eps_map[SI.Z],
    Sweep.B_SET:        si_eps_map[SI.B],
    Sweep.A_SET:        si_eps_map[SI.A],
    Sweep.G_SET:        si_eps_map[SI.G],
    Sweep.LO:           Settings().f0,
    Sweep.SP_FUND:      0,
    Sweep.SP_HARM:      1,
    Sweep.SP_PORT:      1,
    Sweep.SP_POWER:     si_eps_map[SI.A],
    Sweep.TEMP:         300.0,
    Sweep.AVG:          1,
    Sweep.REP:          1,
}

sweep_device_map = {
    Sweep.FREQ:         "cpu",
    Sweep.TIME:         "cpu",
    Sweep.FREQ_M:       "cpu",
    Sweep.TIME_C:       "cpu",
    Sweep.TAU:          "cpu",
    Sweep.PHASE:        "cpu",
    Sweep.V_SET:        "cpu",
    Sweep.I_SET:        "cpu",
    Sweep.Z_SET:        "cpu",
    Sweep.B_SET:        "cpu",
    Sweep.A_SET:        "cpu",
    Sweep.G_SET:        "cpu",
    Sweep.LO:           "cpu",
    Sweep.SP_FUND:      "cpu",
    Sweep.SP_HARM:      "cpu",
    Sweep.SP_PORT:      "cpu",
    Sweep.TEMP:         "cpu",
    Sweep.AVG:          "cpu",
    Sweep.REP:          "cpu",
}

sweep_grad_map = {
    Sweep.FREQ:         True,
    Sweep.TIME:         True,
    Sweep.FREQ_M:       True,
    Sweep.TIME_C:       True,
    Sweep.TAU:          True,
    Sweep.PHASE:        True,
    Sweep.V_SET:        True,
    Sweep.I_SET:        True,
    Sweep.Z_SET:        True,
    Sweep.B_SET:        True,
    Sweep.A_SET:        True,
    Sweep.G_SET:        True,
    Sweep.LO:           True,
    Sweep.SP_FUND:      True,
    Sweep.SP_HARM:      True,
    Sweep.SP_PORT:      True,
    Sweep.TEMP:         True,
    Sweep.AVG:          True,
    Sweep.REP:          True,
}


def sid2p(sweep_id, port_index=None, harm_index=None):
    sweep_name = sweep_name_map[Sweep(sweep_id)]
    sweep_name = sweep_name if port_index is None else sweep_name + "_" + str(port_index)
    sweep_name = sweep_name if harm_index is None else sweep_name + "_" + str(harm_index)
    return sweep_name


def sid2b(sweep_id, port_index=None, harm_index=None):
    return "_" + sid2p(sweep_id, port_index=port_index, harm_index=harm_index)


def p2sid(sweep_name):
    sweep_parts = sweep_name.split('_')
    num_parts = len(sweep_parts)
    index = len(sweep_parts)
    sweep_id = None
    while index > -1:
        try:
            sweep_id = name_sweep_map["_".join(sweep_parts[0:index])]
        except KeyError:
            index -= 1
        else:
            break
    if sweep_id is None:
        raise ValueError("Sweep Name: %s, did not match any supported sweep ids" % (sweep_name,))
    port_index = int(sweep_parts[index]) if index < num_parts else -1
    index += 1
    harm_index = int(sweep_parts[index]) if index < num_parts else -1
    return sweep_id, port_index, harm_index


def p2sib(sweep_name):
    return p2sid(sweep_name[1:])


@unique
class Goal(Flag):
    V_PK = auto()
    I_PK = auto()
    Z_PK = auto()
    V_AVG = auto()
    I_AVG = auto()
    Z_AVG = auto()
    B_PK = auto()
    A_PK = auto()
    G_PK = auto()
    B_AVG = auto()
    A_AVG = auto()
    G_AVG = auto()
    P_DC = auto()
    P_IN = auto()
    P_OUT = auto()
    P_L = auto()
    G_P = auto()
    G_PC = auto()
    EFF = auto()
    PAE = auto()
