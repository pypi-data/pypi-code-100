import torch as th

from sknrf.settings import Settings, InstrumentFlag
from sknrf.enums.runtime import SI, si_dtype_map
from sknrf.enums.signal import transform_color_map
from sknrf.model.transform.base import AbstractTransform
from sknrf.utilities.numeric import Domain


class FFTransform(AbstractTransform):

    _num_ports = -1
    _domain = Domain.FF
    _device = "cpu"
    _preview_filename = ":/PNG/unknown_circuit_transform.png"
    _default_filename = ""
    _color_code = Settings().color_map[transform_color_map[Domain.FF]]
    display_order = ["name", "ports"]
    optimize = True

    def __new__(cls, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL,
                data: th.Tensor = th.eye(2)):
        self = super(FFTransform, cls).__new__(cls, name, ports, instrument_flags=instrument_flags)
        num_points = Settings().t_points*Settings().f_points
        num_ports = len(ports)
        self._abcd = th.eye(num_ports*2, dtype=si_dtype_map[SI.V]).repeat(num_points, 1, 1)
        self._abcd_inv = self._abcd.clone()
        self._data_ = data
        return self

    def __getnewargs__(self):
        state = super(FFTransform, self).__getnewargs__()
        if self.__class__ is FFTransform:
            state = tuple(list(state) +
                         [self._data_])
        return state

    def __init__(self, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL,
                 data: th.Tensor = th.eye(2)):
        super(FFTransform, self).__init__(name, ports, instrument_flags=instrument_flags)
        if self.__class__ == FFTransform:
            self.__info__()
        if data is None:
            self.file = open(self._filename, mode='r')
        else:
            self._set_data(data)

    def __setstate__(self, state):
        if self.__class__ is FFTransform:
            self.__init__(self.name, self.ports, self.instrument_flags,
                          self._data_)

    def __info__(self):
        super(FFTransform, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def _data(self):
        return self._data_

    def _set_data(self, data):
        data = data.repeat(Settings().f_points * Settings().t_points, 1, 1) if data.dim() == 2 else data
        self._abcd = data
        self._abcd_inv = th.inverse(self._abcd)
        self._data_ = data

    @property
    def _min_freq(self):
        return 0 if self.instrument_flags & InstrumentFlag.LF else 1

    @property
    def _max_freq(self):
        return Settings().f_points if self.instrument_flags & InstrumentFlag.RF else 1
