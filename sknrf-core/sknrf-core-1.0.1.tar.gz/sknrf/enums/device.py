from enum import Enum, Flag, auto, unique

import torch as th

from sknrf.enums.runtime import SI, si_dtype_map, si_eps_map
from sknrf.settings import Settings


@unique
class Measurement(Flag):
    SINGLE = auto()
    LS_SP = auto()
    SWEEP = auto()


class Response(Flag):
    V_GET = auto()
    I_GET = auto()
    Z_GET = auto()
    B_GET = auto()
    A_GET = auto()
    G_GET = auto()
    TEMP = auto()
    VIDEO = auto()
    SS_FREQ = auto()
    P = auto()
    PSD = auto()
    SP = auto()
    VIZ_GET = V_GET | I_GET | Z_GET
    VIZ = VIZ_GET
    BAG_GET = B_GET | A_GET | G_GET
    BAG = BAG_GET
    GET = VIZ_GET | BAG_GET
    LS = VIZ | BAG
    DUT = TEMP | VIDEO
    AUX = SS_FREQ | P | PSD | SP


response_name_map = {
    Response.V_GET:   "v",
    Response.I_GET:   "i",
    Response.Z_GET:   "z",
    Response.B_GET:   "b",
    Response.A_GET:   "a",
    Response.G_GET:   "g",
    Response.TEMP:    "temp",
    Response.VIDEO:   "video",
    Response.SS_FREQ: "ss_f",
    Response.P:       "pm",
    Response.PSD:     "sa",
    Response.SP:      "sp",
}

response_shape_map = {
    Response.V_GET:   (Settings().t_points,  Settings().f_points),
    Response.I_GET:   (Settings().t_points,  Settings().f_points),
    Response.Z_GET:   (Settings().t_points,  Settings().f_points),
    Response.B_GET:   (Settings().t_points,  Settings().f_points),
    Response.A_GET:   (Settings().t_points,  Settings().f_points),
    Response.G_GET:   (Settings().t_points,  Settings().f_points),
    Response.TEMP:    (Settings().t_points,  1),
    Response.VIDEO:   (Settings().t_points,  1, Settings().v_cols, Settings().v_rows),
    Response.SS_FREQ: (Settings().t_points, Settings().ss_points, 1, 1),
    Response.P:       (Settings().t_points, 1,                    1, 1),
    Response.PSD:     (Settings().t_points, Settings().ss_points, 1, 1),
    Response.SP:      (Settings().t_points, Settings().ss_points, Settings().ss_num_ports, Settings().ss_num_ports),
}

response_dtype_map = {
    Response.V_GET:   si_dtype_map[SI.V],
    Response.I_GET:   si_dtype_map[SI.I],
    Response.Z_GET:   si_dtype_map[SI.Z],
    Response.B_GET:   si_dtype_map[SI.B],
    Response.A_GET:   si_dtype_map[SI.A],
    Response.G_GET:   si_dtype_map[SI.G],
    Response.TEMP:    si_dtype_map[SI.TEMP],
    Response.VIDEO:   th.double,
    Response.SS_FREQ: si_dtype_map[SI.F],
    Response.P:       th.double,
    Response.PSD:     th.double,
    Response.SP:      th.complex128,
}

response_fill_map = {
    Response.V_GET:   si_eps_map[SI.V],
    Response.I_GET:   si_eps_map[SI.I],
    Response.Z_GET:   si_eps_map[SI.Z],
    Response.B_GET:   si_eps_map[SI.B],
    Response.A_GET:   si_eps_map[SI.A],
    Response.G_GET:   si_eps_map[SI.G],
    Response.TEMP:    si_eps_map[SI.TEMP],
    Response.VIDEO:   th.finfo(response_dtype_map[Response.VIDEO]).eps,
    Response.SS_FREQ: 1.0e9,
    Response.P:       th.finfo(response_dtype_map[Response.P]).eps,
    Response.PSD:     th.finfo(response_dtype_map[Response.PSD]).eps,
    Response.SP:      th.finfo(response_dtype_map[Response.SP]).eps,
}

response_device_map = {
    Response.V_GET:   "cpu",
    Response.I_GET:   "cpu",
    Response.Z_GET:   "cpu",
    Response.B_GET:   "cpu",
    Response.A_GET:   "cpu",
    Response.G_GET:   "cpu",
    Response.TEMP:    "cpu",
    Response.VIDEO:   "cpu",
    Response.SS_FREQ: "cpu",
    Response.P:       "cpu",
    Response.PSD:     "cpu",
    Response.SP:      "cpu",
}

response_grad_map = {
    Response.V_GET:   True,
    Response.I_GET:   True,
    Response.Z_GET:   True,
    Response.B_GET:   True,
    Response.A_GET:   True,
    Response.G_GET:   True,
    Response.TEMP:    True,
    Response.VIDEO:   False,
    Response.SS_FREQ: False,
    Response.P:       False,
    Response.PSD:     False,
    Response.SP:      False,
}


def rid2p(resp_id, port_index=None, harm_index=None):
    resp_name = response_name_map[Response(resp_id)]
    resp_name = resp_name if port_index is None else resp_name + "_" + str(port_index)
    resp_name = resp_name if harm_index is None else resp_name + "_" + str(harm_index)
    return resp_name


def rid2b(resp_id, port_index=None, harm_index=None):
    return "_" + rid2p(resp_id, port_index=port_index, harm_index=harm_index)


def p2rid(resp_id):
    sweep_parts = "_".split(resp_id)
    num_parts = len(sweep_parts)
    index = len(sweep_parts)
    sweep_id = None
    while index > -1:
        try:
            sweep_id = Response("_".join(sweep_parts[0:index]))
        except ValueError:
            index -= 1
        else:
            break
    if sweep_id is None:
        raise ValueError("Sweep Name: %s, did not match any supported sweep ids" % (resp_id,))
    port_index = int(sweep_parts[index]) if index < num_parts else -1
    index += 1
    harm_index = int(sweep_parts[index]) if index < num_parts else -1
    return sweep_id, port_index, harm_index


def p2sib(resp_id):
    return p2rid(resp_id[1:])


class ReceiverZ(Enum):
    _1MOhm = 0
    _50Ohm = 1
