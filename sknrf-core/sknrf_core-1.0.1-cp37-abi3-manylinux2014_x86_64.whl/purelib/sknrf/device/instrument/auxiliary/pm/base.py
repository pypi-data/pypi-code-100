from sknrf.enums.device import Response
from sknrf.device.instrument.auxiliary.base import NoAux


class NoPM(NoAux):
    signal_list = []
    transforms_list = []
    display_order = []

    def __new__(cls, error_model, num_ports, config_filename="", **kwargs):
        self = super(NoPM, cls).__new__(cls, error_model, num_ports, config_filename, **kwargs)
        self.p = None
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoPM, self).__getnewargs__()))

    def __init__(self, error_model, num_ports, config_filename="", **kwargs):
        super(NoPM, self).__init__(error_model, num_ports, config_filename, **kwargs)
        if self.__class__ == NoPM:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoPM, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoPM, self).__setstate__(state)
        if self.__class__ == NoPM:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __info__(self):
        super(NoPM, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["p"].read = False
