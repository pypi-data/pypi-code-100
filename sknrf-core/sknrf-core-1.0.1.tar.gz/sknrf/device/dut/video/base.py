from sknrf.device import AbstractDevice
from sknrf.enums.device import Response
from sknrf.settings import Settings, DeviceFlag
from sknrf.utilities.numeric import AttributeInfo, Info, Scale, Format, PkAvg


class NoVideo(AbstractDevice):

    device_id = DeviceFlag.VIDEO
    signal_list = ["video"]
    transforms_list = []
    display_order = ["on", "dut", "index",
                     "trigger_delay"]

    def __new__(cls, error_model, dut, config_filename="",
                index=0, **kwargs):
        self = super(NoVideo, cls).__new__(cls, error_model, dut, config_filename, **kwargs)
        self.index = index
        self.video = None
        return self

    def __getnewargs__(self):
        args = super(NoVideo, self).__getnewargs__()
        args += (self.index,)
        return args

    def __init__(self, error_model, dut, config_filename="",
                 index=0, **kwargs):
        super(NoVideo, self).__init__(error_model, dut, config_filename, **kwargs)
        self.connect_handles()
        self.__info__()
        self.preset()

        # Initialize object PROPERTIES
        self.initialized = True

    def __getstate__(self, state={}):
        state = super(NoVideo, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoVideo, self).__setstate__(state)
        if self.__class__ == NoVideo:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __info__(self):
        super(NoVideo, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["f0"].read = False
        self.info["num_harmonics"].read = False
        self.info["period"].read = False

        self.info["video"] = Info("video", read=False, write=False, check=False,
                                  format_=Format.RE, scale=Scale._, min_=0, max_=1.0)

    def connect_handles(self):
        super(NoVideo, self).connect_handles()

    def preset(self):
        super(NoVideo, self).preset()
        if self.__class__ == NoVideo:
            pass

    @property
    def dut(self):
        return self.port

    @property
    def num_harmonics(self):
        return Settings().num_harmonics

    @property
    def harmonics(self):
        return Settings().harmonics

    @property
    def freq(self):
        return Settings().freq

    @property
    def time(self):
        return Settings().time
