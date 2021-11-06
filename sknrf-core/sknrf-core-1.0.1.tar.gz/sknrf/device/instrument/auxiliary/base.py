from sknrf.device import AbstractDevice
from sknrf.enums.device import Response, rid2b, rid2p
from sknrf.settings import Settings
from sknrf.utilities.numeric import Info, PkAvg, Format


class NoAux(AbstractDevice):
    signal_list = []
    transforms_list = []
    display_order = []

    def __new__(cls, error_model, num_ports, config_filename="", **kwargs):
        self = super(NoAux, cls).__new__(cls, error_model, num_ports, config_filename, **kwargs)
        self.num_ports = num_ports
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoAux, self).__getnewargs__()))

    def __init__(self, error_model, num_ports, config_filename="", **kwargs):
        super(NoAux, self).__init__(error_model, num_ports, config_filename, **kwargs)
        if self.__class__ == NoAux:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.num_ports = num_ports
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoAux, self).__getstate__(state=state)
        # ### Manually save selected object PROPERTIES here ###
        return state

    def __setstate__(self, state):
        super(NoAux, self).__setstate__(state)
        if self.__class__ == NoAux:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __info__(self):
        super(NoAux, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["num_ports"] = Info("num_ports", read=True, write=False, check=True)
        self.info["f"] = Info("f", read=False, write=False, check=False)

    def connect_handles(self):
        super(NoAux, self).connect_handles()

    def preset(self):
        super(NoAux, self).preset()

    @property
    def num_harmonics(self):
        return Settings().num_harmonics

    @property
    def harmonics(self):
        return Settings().harmonics

    @property
    def f(self):
        return self._error_model._parameters[rid2p(Response.SS_FREQ)]

    @property
    def freq(self):
        return Settings().freq

    @property
    def time(self):
        return Settings().time
