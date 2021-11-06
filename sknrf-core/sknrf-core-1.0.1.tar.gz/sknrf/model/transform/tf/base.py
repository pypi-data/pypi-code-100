import torch as th

from sknrf.settings import Settings, InstrumentFlag
from sknrf.enums.signal import transform_color_map
from sknrf.model.transform.base import AbstractTransform
from sknrf.utilities.numeric import Domain


class TFTransform(AbstractTransform):

    _num_ports = 1
    _domain = Domain.TF
    _device = "cpu"
    _preview_filename = ":/PNG/unknown_circuit_transform.png"
    _default_filename = ""
    _color_code = Settings().color_map[transform_color_map[Domain.TF]]
    display_order = ["name", "ports"]
    optimize = False

    def __new__(cls, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL,
                data: th.Tensor = None):
        self = super(TFTransform, cls).__new__(cls, name, ports, instrument_flags)
        self._data_ = data
        return self

    def __getnewargs__(self):
        state = super(TFTransform, self).__getnewargs__()
        state = tuple(list(state) +
                      [self._data_])
        return state

    def __init__(self, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL,
                 data: th.Tensor = None):
        super(TFTransform, self).__init__(name, ports, instrument_flags)
        if self.__class__ == TFTransform:
            self.__info__()
        if data is not None:
            self._set_data(data)

    def __getstate__(self, state={}):
        super(TFTransform, self).__getstate__(state)
        return state

    def __setstate__(self, state):
        super(TFTransform, self).__setstate__(state)

    def __info__(self):
        super(TFTransform, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

