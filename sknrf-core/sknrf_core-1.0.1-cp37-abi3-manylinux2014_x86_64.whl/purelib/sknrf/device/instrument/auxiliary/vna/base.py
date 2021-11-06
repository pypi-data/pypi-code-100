from sknrf.enums.device import Response
from sknrf.settings import Settings
from sknrf.device.instrument.auxiliary.base import NoAux
from sknrf.utilities.numeric import Info


class NoVNA(NoAux):
    signal_list = []
    transforms_list = []
    display_order = []

    def __new__(cls, error_model, num_ports, config_filename="", **kwargs):
        self = super(NoVNA, cls).__new__(cls, error_model, num_ports, config_filename, **kwargs)
        self.sp = None
        return self

    def __getnewargs__(self):
        return tuple(list(super(NoVNA, self).__getnewargs__()))

    def __init__(self, error_model, num_ports, config_filename="", **kwargs):
        super(NoVNA, self).__init__(error_model, num_ports, config_filename, **kwargs)
        if self.__class__ is NoVNA:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoVNA, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoVNA, self).__setstate__(state)
        if self.__class__ is NoVNA:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __info__(self):
        super(NoVNA, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["num_ports"] = Info("num_ports", read=True, write=True, check=True)
        self.info["sp"].read = False

    @property
    def num_ports(self):
        return self.port

    @num_ports.setter
    def num_ports(self, num_ports):
        self.port = num_ports

    @property
    def trigger_delay(self):
        trigger_delay = self._trigger_delay + self._config["trigger_delay"] + Settings().t_stop
        trigger_delay += self._config["trigger_delay_min"]/10
        return trigger_delay//self._config["trigger_delay_min"]*self._config["trigger_delay_min"]

    @trigger_delay.setter
    def trigger_delay(self, trigger_delay):
        self._trigger_delay = trigger_delay - self._config["trigger_delay"] - Settings().t_stop

