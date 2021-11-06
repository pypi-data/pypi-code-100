from sknrf.device import AbstractDevice
from sknrf.enums.mipi import MIPI_VIO_MODE
from sknrf.device.dut.mipi.server.base import NoMIPIServer
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.dut.video.base import NoVideo
from sknrf.settings import Settings, DeviceFlag
from sknrf.utilities.numeric import Info

__author__ = 'dtbespal'


class NoDUT(AbstractDevice):

    device_id = DeviceFlag.DUT
    signal_list = []
    transforms_list = []
    display_order = ["on", "dut", "batch_id", "wafer_id", "part_id"]

    def __new__(cls, error_model, dut, config_filename="",
                num_mipi=1, num_video=1, **kwargs):
        self = super(NoDUT, cls).__new__(cls, error_model, dut, config_filename, **kwargs)
        self.mipi_driver = ""
        self.mipi_server = None
        self.mipi = [None]*num_mipi
        self.video = [None]*num_video
        self.batch_id = ""
        self.wafer_id = ""
        self.part_id = ""
        self.revision_id = ""
        return self

    def __getnewargs__(self):
        args = super(NoDUT, self).__getnewargs__()
        args += (len(self.mipi), len(self.video))
        return args

    def __init__(self, error_model, dut, config_filename="",
                 num_mipi=2, num_video=1, **kwargs):
        super(NoDUT, self).__init__(error_model, dut, config_filename, **kwargs)
        self.mipi_driver = self._config["mipi_driver"]
        self.mipi_server = eval(self.mipi_driver)(error_model, dut,
                                                  config_filename=self._config["mipi_server_config_filename"])
        self.mipi = [NoMIPIClient(error_model, dut, config_filename=self._config["mipi_config_filename"][i], index=i)
                     for i in range(num_mipi)]
        self.video = [NoVideo(error_model, dut, config_filename=self._config["video_config_filename"][i], index=i)
                      for i in range(num_video)]
        self.connect_handles()
        self.__info__()
        self.preset()

    def __getstate__(self, state={}):
        state = super(NoDUT, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(NoDUT, self).__setstate__(state)
        if self.__class__ == NoDUT:
            self.connect_handles()
            self.__info__()
            self.preset()

            # Initialize object PROPERTIES
            self.initialized = True

    def __info__(self):
        super(NoDUT, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["f0"].read = False
        self.info["num_harmonics"].read = False
        self.info["period"].read = False
        self.info["freq_m"].read = False
        self.info["mipi_driver"] = Info("mipi driver", read=True, write=True, check=False)
        self.info["mipi_server"] = Info("mipi server", read=False, write=False, check=False)
        self.info["mipi"] = Info("mipi", read=False, write=False, check=False)
        self.info["video"] = Info("Video", read=False, write=False, check=False)

        self.info["batch_id"] = Info("batch_id", read=True, write=True, check=False)
        self.info["wafer_id"] = Info("wafer_id", read=True, write=True, check=False)
        self.info["part_id"] = Info("part_id", read=True, write=True, check=False)

    def connect_handles(self):
        super(NoDUT, self).connect_handles()
        self.mipi_server.connect_handles()
        for mipi in self.mipi:
            mipi.connect_handles()
        for video in self.video:
            video.connect_handles()

    def disconnect_handles(self):
        super(NoDUT, self).disconnect_handles()
        for video in self.video:
            video.disconnect_handles()
        for mipi in self.mipi:
            mipi.disconnect_handles()
        self.mipi_server.disconnect_handles()

    def preset(self):
        super(NoDUT, self).preset()
        if self.__class__ == NoDUT:
            self.mipi_server.preset()
            for mipi in self.mipi:
                mipi.preset()
            for video in self.video:
                video.preset()

    @property
    def dut(self):
        return self.port

    def stimulus(self):
        pass

    def measure(self):
        pass
