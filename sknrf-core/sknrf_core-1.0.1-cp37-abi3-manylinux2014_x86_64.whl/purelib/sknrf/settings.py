import os
import sys
from enum import Flag, auto
import subprocess
from subprocess import Popen

import torch as th
import yaml
from PySide2 import QtCore
from PySide2.QtCore import QObject, QMutex
from qtpropertybrowser import Format, Scale

from sknrf.enums.runtime import SI, si_eps_map, si_dtype_map, RuntimeState, Bound
from sknrf.utilities.numeric import AttributeInfo, Info
from sknrf.utilities.patterns import SingletonType, synchronized


class DeviceFlag(Flag):
    NONE = 0
    LFSOURCE = auto()
    LFRECEIVER = auto()
    LFZTUNER = auto()
    RFSOURCE = auto()
    RFRECEIVER = auto()
    RFZTUNER = auto()
    DUT = auto()
    MIPI_CLIENT = auto()
    MIPI_SERVER = auto()
    VIDEO = auto()
    LF = LFSOURCE | LFRECEIVER | LFZTUNER
    RF = RFSOURCE | RFRECEIVER | RFZTUNER
    SOURCE = LFSOURCE | RFSOURCE
    RECEIVER = LFRECEIVER | RFRECEIVER
    ZTUNER = LFZTUNER | RFZTUNER
    STIMULUS = SOURCE | ZTUNER
    RESPONSE = RECEIVER
    INSTRUMENT = STIMULUS | RESPONSE
    MIPI = MIPI_CLIENT | MIPI_SERVER
    SUB_DUT = MIPI | VIDEO
    ALL = INSTRUMENT | DUT | SUB_DUT


device_name_map = {DeviceFlag.LFSOURCE: "lfsource",
                   DeviceFlag.LFRECEIVER: "lfreceiver",
                   DeviceFlag.LFZTUNER: "lfztuner",
                   DeviceFlag.RFSOURCE: "rfsource",
                   DeviceFlag.RFRECEIVER: "rfreceiver",
                   DeviceFlag.RFZTUNER: "rfztuner",
                   DeviceFlag.DUT: "dut",
                   DeviceFlag.MIPI_CLIENT: "mipi_client",
                   DeviceFlag.MIPI_SERVER: "mipi_server",
                   DeviceFlag.VIDEO: "video",
                   }
device_icon_map = {DeviceFlag.LFSOURCE: ":/PNG/black/64/lfsource.png",
                   DeviceFlag.LFRECEIVER: ":/PNG/black/64/lfreceiver.png",
                   DeviceFlag.LFZTUNER: ":/PNG/black/64/lfztuner.png",
                   DeviceFlag.RFSOURCE: ":/PNG/black/64/rfsource.png",
                   DeviceFlag.RFRECEIVER: ":/PNG/black/64/rfreceiver.png",
                   DeviceFlag.RFZTUNER: ":/PNG/black/64/rfztuner.png",
                   DeviceFlag.DUT: ":/PNG/black/64/dut.png",
                   DeviceFlag.MIPI_CLIENT: ":/PNG/black/64/mip_client.png",
                   DeviceFlag.MIPI_SERVER: ":/PNG/black/64/mipi_server.png",
                   DeviceFlag.VIDEO: ":/PNG/black/64/video.png",
                   }


class InstrumentFlag(Flag):
    NONE = 0
    LFSOURCE = auto()
    LFRECEIVER = auto()
    LFZTUNER = auto()
    RFSOURCE = auto()
    RFRECEIVER = auto()
    RFZTUNER = auto()
    LF = LFSOURCE | LFRECEIVER | LFZTUNER
    RF = RFSOURCE | RFRECEIVER | RFZTUNER
    SOURCE = LFSOURCE | RFSOURCE
    RECEIVER = LFRECEIVER | RFRECEIVER
    ZTUNER = LFZTUNER | RFZTUNER
    STIMULUS = SOURCE | ZTUNER
    RESPONSE = RECEIVER
    ALL = STIMULUS | RESPONSE


instrument_name_map = {InstrumentFlag.LFSOURCE: "lfsource",
                       InstrumentFlag.LFRECEIVER: "lfreceiver",
                       InstrumentFlag.LFZTUNER: "lfztuner",
                       InstrumentFlag.RFSOURCE: "rfsource",
                       InstrumentFlag.RFRECEIVER: "rfreceiver",
                       InstrumentFlag.RFZTUNER: "rfztuner",
                       }
instrument_icon_map = {InstrumentFlag.LFSOURCE: ":/PNG/black/64/lfsource.png",
                       InstrumentFlag.LFRECEIVER: ":/PNG/black/64/lfreceiver.png",
                       InstrumentFlag.LFZTUNER: ":/PNG/black/64/lfztuner.png",
                       InstrumentFlag.RFSOURCE: ":/PNG/black/64/rfsource.png",
                       InstrumentFlag.RFRECEIVER: ":/PNG/black/64/rfreceiver.png",
                       InstrumentFlag.RFZTUNER: ":/PNG/black/64/rfztuner.png"
                       }


class Settings(QObject, metaclass=SingletonType):
    """Settings

        Defines an object containing all measurement global settings

        Attributes
        ----------
        precision : int
            The number of digits after the decimal place in scientific notation.
        bound : sknrf.enums.runtime.Bound
            Increase level of bound checking to increase the amount of numerical stability checks.
        debug : bool
            Debug mode enable flag.
        environment: str
            Anaconda virtual environment for executing shell commands.
        root : str
            Absolute path to root directory where all sknrf src files are stored.
        data_root : str
            Absolute path to data root director where all sknrf data files are stored
        url_root : str
            Absolute URL to sknrf website.
        url_api : str
            Relative URL from Settings().url_root to the programmable API
        on_order : list
            List of strings denoting the orderfor turning on the devices.
        off_order : list
            List of strings denoting the order for turning of the devices.
        netlist_filename : str
            Relative filenmae from the Settings().data_root to the simulation netlist file.
        dataset_filename : str
            Relative filename frmo the Settings().data_root to the simulation dataset file.
        remote_host : str
            Remote host URL.
        remote_user : str
            Remote host login username.
        remote_passord : Optional[str]
            Remote host login password for unsecure login.
        remote_key_filename : Optional[str]
            Absolute filename of SSH RSA public key for secure remote login (without password entry).
        remote_port : int
            Remote host port number, default is 2222
        color_order : list
            Default color order.
        color_map : dict
            Dictionary mapping from color name to RGB color codes
        line_order : list
            Default line order.
        marker_order : list
            Default marker order.
    """
    device_reset_requested = QtCore.Signal()
    device_reset_required = QtCore.Signal()
    _default_on_order = ["LFSource", "RFSource", "LFZTuner", "RFZTuner"]
    color_order = ["blue", "green", "red", "violet", "cyan", "yellow", "magenta", "black"]
    color_map = {
        "blue": '#268bd2',
        "green": '#859900',
        "orange": '#cb4b16',
        "red": '#dc322f',
        "cyan": '#2aa198',
        "magenta": '#d33682',
        "violet": '#6c71c4',
        "yellow": '#b58900',
        "black": '#000000',
        "white": '#FFFFFF'
    }
    line_order = ["-", "--", "-.", ":"]
    marker_order = ['x', '+', '1', '3', 'o', 's', '^', 'D']
    display_order = ["debug", "runtime_state", "num_ports", "num_mipi", "num_duts", "num_video", "precision", "bound",  # Genaeral
                     "f0", "num_harmonics", "f_points",  # Frequency
                     "t_step", "t_stop", "t_points", "t_rise", "t_fall",  # Time
                     "lock_lo", "trigger_port", "trigger_device", "z0",  # RF
                     "ss_num_ports", "ss_power", "ss_f0", "ss_span", "ss_points", "ss_harm", "ss_ref", "ss_mod", "ss_realtime",  # SS
                     "v_cols", "v_rows",  # Video
                     "realtime", "sweep_avg", "signal_avg", "sweep_rep", "signal_rep", "max_iter",  # Iterations
                     "datagroup", "dataset", "environment", "root", "data_root", "url_root", "url_api",  # Database
                     "on_order", "off_order", "ss_on_order", "ss_off_order",
                     "netlist_filename", "dataset_filename", # Simulation
                     "remote_host", "remote_user", "remote_password", "remote_key_filename", "remote_port",  # Remote
                     "color_map", "color_order", "line_order", "marker_order",]  # Display

    def __new__(cls, filename=""):
        self = super(Settings, cls).__new__(cls)
        self.lock = QMutex()
        self._runtime_state = RuntimeState.STOPPED
        self._debug = True
        self.background = False
        self._qt_logging_handler = None
        self._request_response = False
        self.info = None

        self._precision = 3
        self._bound = Bound.OFF

        self._num_ports = 2
        self._num_mipi = 1
        self._num_duts = 1
        self._num_video = 1
        self._t_step = 10e-6
        self._t_stop = 10e-6
        self._t_rise = 0.0
        self._t_fall = 0.0
        self._f0 = 1.0e9
        self._num_harmonics = 3
        self.__set_time()
        self.__set_freq()
        self._trigger_port = 1
        self._trigger_device = "rfreceiver"
        self._z0 = 50

        self._realtime = False
        self._sweep_avg = 1
        self._signal_avg = 1
        self._sweep_rep = 1
        self._signal_rep = 1
        self._max_iter = 1

        self._lock_lo = False

        self._ss_num_ports = 2
        self._ss_power = 0.001
        self._ss_f0 = 1.0e9
        self._ss_span = 100e6
        self._ss_points = 2
        self._ss_harm = "all"
        self._ss_ref = "receiver"
        self._ss_mod = "phasor"
        self._ss_realtime = False

        self.v_cols = 512
        self.v_rows = 512

        self._environment = "root"
        self.root = ""
        self.data_root = ""
        self.url_root = ""
        self.url_api = ""
        self._datagroup = ""
        self._dataset = ""
        self._sys_path = sys.path.copy()
        self._ext_path = []

        self._off_order = []
        self._on_order = []
        self._ss_on_order = []
        self._ss_off_order = []

        self.netlist_filename = ""
        self.dataset_filename = ""
        self.remote_host = ""
        self.remote_user = ""
        self.remote_password = ""
        self.remote_key_filename = ""
        self.remote_port = 2222

        return self

    def __init__(self, filename=""):
        super(Settings, self).__init__()
        self.load(filename)

    def __info__(self):
        self.info = AttributeInfo.initialize(self, self.display_order)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["info"].read = False
        self.info["device_reset_requested"].read = False
        self.info["device_reset_required"].read = False
        self.info["lock"].read = False
        self.info["display_order"].read = False

        self.info["precision"] = Info("precision", read=True, write=True, check=False)
        self.info["bound"] = Info("bound", read=True, write=True, check=False)

        self.info["package_map"] = Info("package_map", read=False, write=False, check=False)
        self.info["debug"] = Info("debug", read=True, write=True, check=False, format_=Format.RE)
        self.info["num_ports"] = Info("num_ports", read=True, write=True, check=False, format_=Format.RE)
        self.info["num_mipi"] = Info("num_mipi", read=True, write=True, check=False, format_=Format.RE)
        self.info["num_duts"] = Info("num_duts", read=True, write=True, check=False, format_=Format.RE)
        self.info["num_video"] = Info("num_video", read=True, write=True, check=False, format_=Format.RE)
        self.info["f0"] = Info("f0", read=True, write=True, check=False, format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["num_harmonics"] = Info("num_harmonics", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["f_points"] = Info("f_points", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["t_step"] = Info("t_step", read=True, write=True, check=False, format_=Format.RE, scale=Scale.u, unit="s")
        self.info["t_stop"] = Info("t_stop", read=True, write=True, check=False, format_=Format.RE, scale=Scale.u, unit="s")
        self.info["t_rise"] = Info("t_rise", read=True, write=True, check=False, format_=Format.RE, scale=Scale.u, unit="s")
        self.info["t_fall"] = Info("t_fall", read=True, write=True, check=False, format_=Format.RE, scale=Scale.u, unit="s")
        self.info["t_points"] = Info("t_points", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["harmonics"] = Info("harmonics", read=False, write=False, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["freq"] = Info("freq", read=False, write=False, check=False, format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["time_c"] = Info("time_c", read=False, write=False, check=False, format_=Format.RE, scale=Scale.n, unit="s")
        self.info["time"] = Info("time", read=False, write=False, check=False, format_=Format.RE, scale=Scale._, unit="s")
        self.info["freq_m"] = Info("freq_m", read=False, write=False, check=False, format_=Format.RE, scale=Scale.M, unit="Hz")

        self.info["ss_num_ports"] = Info("ss_num_ports", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["ss_power"] = Info("ss_power", read=True, write=True, check=False, format_=Format.LOG_DEG, scale=Scale.m, unit="rW")
        self.info["ss_f0"] = Info("ss f0", read=True, write=True, check=False, format_=Format.RE, scale=Scale.G, unit="Hz")
        self.info["ss_span"] = Info("ss span", read=True, write=True, check=False, format_=Format.RE, scale=Scale.M, unit="Hz")
        self.info["ss_points"] = Info("ss_points", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["ss_harm"] = Info("ss_harm", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["ss_ref"] = Info("ss_ref", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["ss_mod"] = Info("ss_mod", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["ss_realtime"] = Info("ss_realtime", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")

        self.info["v_cols"] = Info("v_cols", read=True, write=False, check=False, format_=Format.RE, scale=Scale._, unit="px")
        self.info["v_rows"] = Info("v_rows", read=True, write=False, check=False, format_=Format.RE, scale=Scale._, unit="px")

        self.info["trigger_device"] = Info("trigger_device", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")
        self.info["trigger_port"] = Info("trigger_port", read=True, write=True, check=False, format_=Format.RE, scale=Scale._, unit="")

        self.info["lock_lo"] = Info("lock LO", read=True, write=True, check=False)

    def __getstate__(self, state={}):

        state["precision"] = self._precision
        state["bound"] = self._bound

        state["debug"] = self._debug
        state["num_ports"] = self._num_ports
        state["num_mipi"] = self.num_mipi
        state["num_duts"] = self._num_duts
        state["num_video"] = self._num_video
        state["t_step"] = self._t_step
        state["t_stop"] = self._t_stop
        state["t_rise"] = self._t_rise
        state["t_fall"] = self._t_fall
        state["f0"] = self._f0
        state["num_harmonics"] = self._num_harmonics
        state["trigger_device"] = self._trigger_device
        state["trigger_port"] = self._trigger_port
        state["z0"] = self._z0

        state["realtime"] = self._realtime
        state["sweep_avg"] = self._sweep_avg
        state["signal_avg"] = self._signal_avg
        state["sweep_rep"] = self._sweep_rep
        state["signal_rep"] = self._signal_rep
        state["max_iter"] = self._max_iter

        state["lock_lo"] = self._lock_lo

        state["ss_num_ports"] = self._ss_num_ports
        state["ss_power"] = self._ss_power
        state["ss_f0"] = self._ss_f0
        state["ss_span"] = self._ss_span
        state["ss_points"] = self._ss_points
        state["ss_harm"] = self._ss_harm
        state["ss_ref"] = self._ss_ref
        state["ss_mod"] = self._ss_mod
        state["ss_realtime"] = self._ss_realtime

        state["v_cols"] = self.v_cols
        state["v_rows"] = self.v_rows

        state["environment"] = self._environment
        state["root"] = os.path.expandvars(self.root)
        state["data_root"] = os.path.expandvars(self.data_root)
        state["url_root"] = os.path.expandvars(self.url_root)
        state["url_api"] = self.url_api
        state["datagroup"] = self._datagroup
        state["dataset"] = self._dataset
        state["_sys_path"] = self._sys_path
        state["ext_path"] = self._ext_path

        state["off_order"] = self.off_order
        state["on_order"] = self.on_order
        state["ss_off_order"] = self.ss_off_order
        state["ss_on_order"] = self.ss_on_order

        state["netlist_filename"] = os.path.expandvars(self.netlist_filename)
        state["dataset_filename"] = os.path.expandvars(self.dataset_filename)
        state["remote_host"] = self.remote_host
        state["remote_user"] = self.remote_user
        state["remote_key_filename"] = self.remote_key_filename
        return state

    def __setstate__(self, state):
        self.__info__()
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        self._precision = state["precision"]
        self._bound = state["bound"]

        self._debug = state["debug"]
        self._num_ports = state["num_ports"]
        self._num_mipi = state["num_mipi"]
        self._num_duts = state["num_duts"]
        self._num_video = state["num_video"]
        self._t_step = state["t_step"]
        self._t_stop = state["t_stop"]
        self._t_rise = state["t_rise"]
        self._t_fall = state["t_fall"]
        self._f0 = state["f0"]
        self._num_harmonics = state["num_harmonics"]
        self.__set_time()
        self.__set_freq()
        self._trigger_port = state["trigger_port"]
        self._trigger_device = state["trigger_device"]
        self._z0 = state["z0"]

        self._realtime = state["realtime"]
        self._sweep_avg = state["sweep_avg"]
        self._signal_avg = state["signal_avg"]
        self._sweep_rep = state["sweep_rep"]
        self._signal_rep = state["signal_rep"]
        self._max_iter = state["max_iter"]

        self._lock_lo = state["lock_lo"]

        self._ss_num_ports = state["ss_num_ports"]
        self._ss_power = state["ss_power"]
        self._ss_f0 = state["ss_f0"]
        self._ss_span = state["ss_span"]
        self._ss_points = state["ss_points"]
        self._ss_harm = state["ss_harm"]
        self._ss_ref = state["ss_ref"]
        self._ss_mod = state["ss_mod"]
        self._ss_realtime = state["ss_realtime"]

        self.v_cols = state["v_cols"]
        self.v_rows = state["v_rows"]

        self._environment = state["environment"]
        self.root = os.path.expandvars(state["root"])
        self.data_root = os.path.expandvars(state["data_root"])
        self.url_root = os.path.expandvars(state["url_root"])
        self.url_api = state["url_api"]
        self._datagroup = state["datagroup"]
        self._dataset = state["dataset"]
        self._sys_path = state["_sys_path"].copy() if "_sys_path" in state else sys.path.copy()
        sys.path = self._sys_path.copy()
        self.ext_path = state["ext_path"]

        self.off_order = state["off_order"]
        self.on_order = state["on_order"]
        self.ss_off_order = state["ss_off_order"]
        self.ss_on_order = state["ss_on_order"]

        self.netlist_filename = os.path.expandvars(state["netlist_filename"])
        self.dataset_filename = os.path.expandvars(state["dataset_filename"])
        self.remote_host = state["remote_host"]
        self.remote_user = state["remote_user"]
        self.remote_key_filename = state["remote_key_filename"]

    def load(self, filename=""):
        if len(filename) == 0 and "SKNRF_CONFIG" in os.environ:
            filename = os.environ["SKNRF_CONFIG"]
        elif len(filename) == 0:
            filename = os.sep.join((os.getcwd(), "sknrf.yml"))
        with open(filename) as f:
            self.__setstate__(yaml.safe_load(f))

    @property
    @synchronized(None)
    def runtime_state(self):
        return self._runtime_state

    @runtime_state.setter
    @synchronized(None)
    def runtime_state(self, state):
        self._runtime_state = state

    @property
    @synchronized(None)
    def debug(self):
        """int: The debug level.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._debug

    @debug.setter
    @synchronized(None)
    def debug(self, debug):
        assert(isinstance(debug, bool))
        self.set_critical_property("_debug", debug)

    @property
    def system_buffers(self):
        """int: The os.system() buffers
        """
        if self._debug:
            return ""
        else:
            return " >/dev/null 2>&1"

    @property
    def subprocess_buffers(self):
        """int: The subprocess buffers
        """
        if self._debug:
            return {}
        else:
            return {"stdout": subprocess.DEVNULL, "stderr": subprocess.STDOUT}

    @property
    @synchronized(None)
    def num_ports(self):
        """int: The number of measurement ports.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._num_ports

    @num_ports.setter
    @synchronized(None)
    def num_ports(self, num_ports):
        assert(isinstance(num_ports, int) and num_ports >= 1)
        self.set_critical_property("_num_ports", num_ports)

    @property
    @synchronized(None)
    def num_mipi(self):
        """int: The number of mipi devices.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._num_mipi

    @num_mipi.setter
    @synchronized(None)
    def num_mipi(self, num_mipi):
        assert (isinstance(num_mipi, int) and num_mipi >= 1)
        self.set_critical_property("_num_mipi", num_mipi)

    @property
    @synchronized(None)
    def num_duts(self):
        """int: The number of devices-under-test being measured.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._num_duts

    @num_duts.setter
    @synchronized(None)
    def num_duts(self, num_duts):
        assert(isinstance(num_duts, int) and num_duts >= 1)
        self.set_critical_property("_num_duts", num_duts)

    @property
    @synchronized(None)
    def num_video(self):
        """int: The number of video cameras.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._num_video

    @num_video.setter
    @synchronized(None)
    def num_video(self, num_video):
        assert (isinstance(num_video, int) and num_video >= 1)
        self.set_critical_property("_num_video", num_video)

    @property
    @synchronized(None)
    def f0(self):
        """float: The fundamental carrier measurement frequency ($$1f_0$$).

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._f0

    @f0.setter
    @synchronized(None)
    def f0(self, f0):
        assert(f0 > 0)
        self.set_critical_property("_f0", f0)

    @property
    @synchronized(None)
    def num_harmonics(self):
        """int: The harmonic measurement frequencies ($$n$$)

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._num_harmonics

    @num_harmonics.setter
    @synchronized(None)
    def num_harmonics(self, num_harmonics):
        i_num_harmonics = int(num_harmonics)
        assert(i_num_harmonics > 0)
        self.set_critical_property("_num_harmonics", i_num_harmonics)


    @num_harmonics.setter
    @synchronized(None)
    def num_harmonics(self, num_harmonics):
        i_num_harmonics = int(num_harmonics)
        assert (i_num_harmonics > 0)
        self.set_critical_property("_num_harmonics", i_num_harmonics)

    @property
    @synchronized(None)
    def f_points(self):
        """int: The number of points in the frequency sweep (= Settings().num_harmonics + 1).

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._freq.shape[-1]

    @f_points.setter
    @synchronized(None)
    def f_points(self, f_points):
        i_f_points = int(f_points)
        assert(i_f_points > 1)
        i_num_harmonics = i_f_points-1
        self.set_critical_property("_num_harmonics", i_num_harmonics)

    @property
    @synchronized(None)
    def freq(self):
        """ndarray[float]: The frequency sweep array (Settings().f_points, 1).
        """
        return self._freq

    @property
    @synchronized(None)
    def time_c(self):
        cycles, points = 2, 25
        num_harmonics = self._num_harmonics + 1
        nfft = points * num_harmonics
        tc_stop = cycles/self._f0
        time_c = th.linspace(0, tc_stop, cycles*nfft, dtype=si_dtype_map[SI.T])
        return time_c

    @property
    @synchronized(None)
    def harmonics(self):
        """ndarray[int]: The harmonic sweep array (Settings().f_points,).
        """
        return th.arange(0, self._freq.shape[-1], 1, dtype=th.int)

    @property
    @synchronized(None)
    def t_step(self):
        """float: The step in the time sweep (> 0).

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._t_step

    @t_step.setter
    @synchronized(None)
    def t_step(self, t_step):
        assert(t_step > 0)
        self.set_critical_property("_t_step", t_step)

    @property
    @synchronized(None)
    def t_stop(self):
        """float: The length of the time sweep (>= 0).

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._t_stop

    @t_stop.setter
    @synchronized(None)
    def t_stop(self, t_stop):
        assert(t_stop >= 0)
        self.set_critical_property("_t_stop", t_stop)

    @property
    @synchronized(None)
    def t_rise(self):
        """float: The rise time of the transient.
        """
        return self._t_rise

    @t_rise.setter
    @synchronized(None)
    def t_rise(self, t_rise):
        self._t_rise = min(max(0, t_rise), self._t_stop)

    @property
    @synchronized(None)
    def t_fall(self):
        """float: The fall time of the transient.
        """
        return self._t_fall

    @t_fall.setter
    @synchronized(None)
    def t_fall(self, t_fall):
        self._t_fall = min(max(0, t_fall), self._t_stop)

    @property
    @synchronized(None)
    def t_points(self):
        """int: The number of points in the time sweep.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._time.shape[-2]

    @t_points.setter
    @synchronized(None)
    def t_points(self, t_points):
        i_t_points = int(t_points)
        assert(i_t_points > 0)
        t_step = self._t_stop/(i_t_points-1)
        self.set_critical_property("_t_step", t_step)

    @property
    @synchronized(None)
    def time(self):
        """ndarray[float]: The time sweep array (Settings().t_points, 1).
        """
        return self._time

    @property
    @synchronized(None)
    def freq_m(self):
        t_step = self._t_step
        fm_start = -1 / (2 * t_step)
        fm_stop = 1 / (2 * t_step)
        fm_step = 1 / self._t_stop
        fm_points = int(round((fm_stop - fm_start) / fm_step + 1))
        freq_m = th.linspace(fm_start, fm_stop, fm_points, dtype=si_dtype_map[SI.F]).reshape(-1, 1)
        return freq_m

    @property
    @synchronized(None)
    def on_order(self):
        return self._on_order

    @on_order.setter
    @synchronized(None)
    def on_order(self, on_order):
        default_order = ["%s%d" % (device_name, port_index)
                         for device_name in self._default_on_order
                         for port_index in range(self._num_ports + 1)]
        new_order = []
        for device_id in on_order:
            try:
                new_order.append(default_order.pop(default_order.index(device_id)))
            except ValueError:
                pass
        self._on_order = new_order + default_order

    @property
    @synchronized(None)
    def off_order(self):
        return self._off_order

    @off_order.setter
    @synchronized(None)
    def off_order(self, off_order):
        default_order = ["%s%d" % (device_name, port_index)
                         for device_name in reversed(self._default_on_order)
                         for port_index in reversed(range(self._num_ports + 1))]
        new_order = []
        for device_id in off_order:
            try:
                new_order.append(default_order.pop(default_order.index(device_id)))
            except ValueError:
                pass
        self._off_order = new_order + default_order

    @property
    @synchronized(None)
    def ss_on_order(self):
        return self._ss_on_order

    @ss_on_order.setter
    @synchronized(None)
    def ss_on_order(self, ss_on_order):
        default_order = ["%s" % (device_name,)
                         for device_name in self._default_on_order]
        new_order = []
        for device_id in ss_on_order:
            try:
                new_order.append(default_order.pop(default_order.index(device_id)))
            except ValueError:
                pass
        self._ss_on_order = new_order + default_order

    @property
    @synchronized(None)
    def ss_off_order(self):
        return self._ss_off_order

    @ss_off_order.setter
    @synchronized(None)
    def ss_off_order(self, ss_off_order):
        default_order = ["%s" % (device_name,)
                         for device_name in reversed(self._default_on_order)]
        new_order = []
        for device_id in ss_off_order:
            try:
                new_order.append(default_order.pop(default_order.index(device_id)))
            except ValueError:
                pass
        self._ss_off_order = new_order + default_order

    @property
    @synchronized(None)
    def ss_num_ports(self):
        """float: The number of small-signal ports.
        """
        return self._ss_num_ports

    @ss_num_ports.setter
    @synchronized(None)
    def ss_num_ports(self, ss_num_ports):
        self._ss_num_ports = ss_num_ports

    @property
    @synchronized(None)
    def ss_power(self):
        """float: The power level of small-signal measurements.
        """
        return self._ss_power

    @ss_power.setter
    @synchronized(None)
    def ss_power(self, ss_power):
        self._ss_power = ss_power

    @property
    @synchronized(None)
    def ss_f0(self):
        """float: The center frequency of the auxiliary measurement.
        """
        return self._ss_f0

    @ss_f0.setter
    @synchronized(None)
    def ss_f0(self, ss_f0):
        self._ss_f0 = ss_f0

    @property
    @synchronized(None)
    def ss_span(self):
        """float: The frequency span of the auxiliary measurement.
        """
        return self._ss_span

    @ss_span.setter
    @synchronized(None)
    def ss_span(self, ss_span):
        self._ss_span = ss_span

    @property
    @synchronized(None)
    def ss_points(self):
        """int: The number of points in the time sweep.

            Note:
                Setting this property will reset the application and disable any measurement correction.
        """
        return self._ss_points

    @ss_points.setter
    @synchronized(None)
    def ss_points(self, ss_points):
        i_ss_points = int(ss_points)
        assert (i_ss_points > 0)
        self.set_critical_property("_ss_points", i_ss_points)

    @property
    @synchronized(None)
    def ss_harm(self):
        """str: The harmonic setting of the ss measurement.
        """
        return self._ss_harm

    @ss_harm.setter
    @synchronized(None)
    def ss_harm(self, ss_harm):
        self._ss_harm = ss_harm

    @property
    @synchronized(None)
    def ss_ref(self):
        """str: The reference signal of the ss measurement.
        """
        return self._ss_ref

    @ss_ref.setter
    @synchronized(None)
    def ss_ref(self, ss_ref):
        self._ss_ref = ss_ref

    @property
    @synchronized(None)
    def ss_mod(self):
        """bool: Realtime ss measurement enable.
        """
        return self._ss_mod

    @ss_mod.setter
    @synchronized(None)
    def ss_mod(self, ss_mod):
        self._ss_mod = ss_mod

    @property
    @synchronized(None)
    def ss_realtime(self):
        """bool: Realtime ss measurement enable.
        """
        return self._ss_realtime

    @ss_realtime.setter
    @synchronized(None)
    def ss_realtime(self, ss_realtime):
        self._ss_realtime = ss_realtime

    @property
    @synchronized(None)
    def trigger_device(self):
        """str: The name of the device that triggers a measurement.
        """
        return DeviceFlag(2**list(device_name_map.values()).index(self._trigger_device))

    @trigger_device.setter
    @synchronized(None)
    def trigger_device(self, trigger_device):
        self._trigger_device = device_name_map[trigger_device]

    @property
    @synchronized(None)
    def trigger_port(self):
        """int: The port index of the instrument that triggers a measurement.
        """
        return self._trigger_port

    @trigger_port.setter
    @synchronized(None)
    def trigger_port(self, trigger_port):
        self._trigger_port = trigger_port

    @property
    @synchronized(None)
    def z0(self):
        return self._z0

    @z0.setter
    @synchronized(None)
    def z0(self, z0):
        self._z0 = z0

    @property
    @synchronized(None)
    def realtime(self):
        return self._realtime

    @realtime.setter
    @synchronized(None)
    def realtime(self, realtime):
        self._realtime = realtime

    @property
    @synchronized(None)
    def sweep_avg(self):
        return self._sweep_avg

    @sweep_avg.setter
    @synchronized(None)
    def sweep_avg(self, sweep_avg):
        self._sweep_avg = max(sweep_avg, 1)

    @property
    @synchronized(None)
    def signal_avg(self):
        return self._signal_avg

    @signal_avg.setter
    @synchronized(None)
    def signal_avg(self, signal_avg):
        self._signal_avg = max(signal_avg, 1)

    @property
    @synchronized(None)
    def signal_avg(self):
        return self._signal_avg

    @signal_avg.setter
    @synchronized(None)
    def signal_avg(self, signal_avg):
        self._signal_avg = max(signal_avg, 1)

    @property
    @synchronized(None)
    def sweep_rep(self):
        return self._sweep_rep

    @sweep_rep.setter
    @synchronized(None)
    def sweep_rep(self, sweep_rep):
        self._sweep_rep = max(sweep_rep, 1)

    @property
    @synchronized(None)
    def signal_rep(self):
        return self._signal_rep

    @signal_rep.setter
    @synchronized(None)
    def signal_rep(self, signal_rep):
        self.signal_rep = max(signal_rep, 0)

    @property
    @synchronized(None)
    def max_iter(self):
        return self._max_iter

    @max_iter.setter
    @synchronized(None)
    def max_iter(self, max_iter):
        self._max_iter = max(max_iter, 1)

    @property
    @synchronized(None)
    def lock_lo(self):
        return self._lock_lo

    @lock_lo.setter
    @synchronized(None)
    def lock_lo(self, lock_lo):
        self._lock_lo = lock_lo

    @property
    @synchronized(None)
    def datagroup(self):
        """str: The name of the current datagroup where measurements are stored.
        """
        return self._datagroup

    @datagroup.setter
    @synchronized(None)
    def datagroup(self, datagroup):
        self._datagroup = datagroup

    @property
    @synchronized(None)
    def dataset(self):
        """str: The name of the current dataset where measurements are stored.
        """
        return self._dataset

    @dataset.setter
    @synchronized(None)
    def dataset(self, dataset):
        self._dataset = dataset

    @property
    @synchronized(None)
    def ext_path(self):
        """list: The extension path
        """
        return self._ext_path

    @ext_path.setter
    @synchronized(None)
    def ext_path(self, ext_path):
        self._ext_path = []
        for path in reversed(ext_path):
            path = os.path.expandvars(path)
            if path not in sys.path:
                sys.path.insert(0, path)
                self._ext_path.insert(0, path)

    @property
    @synchronized(None)
    def precision(self):
        """int: The number of digits displayed after the decimal point.
        """
        return self._precision

    @precision.setter
    @synchronized(None)
    def precision(self, precision):
        assert(isinstance(precision, int) and precision > 0)
        self._precision = precision

    @property
    @synchronized(None)
    def bound(self):
        """sknrf.enums.runtime.Bound: Increase level of bound checking to increase the amount of numerical stability checks.
        """
        return Bound(self._bound)

    @bound.setter
    @synchronized(None)
    def bound(self, bound):
        self._bound = bound

    @property
    @synchronized(None)
    def environment(self):
        return self._environment

    @environment.setter
    @synchronized(None)
    def environment(self, environment):
        old_env = self._environment
        try:
            self._environment = environment
            self.system("pwd")
        except OSError:
            self._environment = old_env

    def set_request_response(self, response):
        """Sets the temporary state of the user request response dialog.

            Parameters
            ----------
            response : bool
            user request response.
        """
        self._request_response = response

    def set_critical_property(self, name, new_value):
        """Resets the measurement system.

            When a critical property is set, the measurement system state must be reset. A system reset will reset the
            following:

                * The frequency sweep.
                * The time sweep.
                * The error correction.

            Parameters
            ----------
            response : bool
            user request response.
        """
        if new_value != getattr(self, name):
            self.lock.unlock()
            try:
                self.device_reset_requested.emit()
                if self._request_response or self.signalsBlocked() or self.background:
                    self._request_response = False
                    setattr(self, name, new_value)
                    self.__set_freq()
                    self.__set_time()
                    self.off_order = []
                    self.on_order = []
                    self.ss_off_order = []
                    self.ss_on_order = []
                    self.device_reset_required.emit()
            finally:
                self.lock.lock()

    def __set_time(self):
        """Calculates the time sweep.
        """
        calc_t_stop = max(max(round(self._t_stop/self._t_step)*self._t_step, self._t_stop), self._t_step)
        calc_t_points = round(calc_t_stop/self._t_step)+1
        self._time = th.linspace(0, calc_t_stop, int(calc_t_points), dtype=si_dtype_map[SI.T]).reshape((-1, 1))

    def __set_freq(self):
        """Calculates the frequency sweep.
        """
        self._freq = th.arange(0, self._f0*(self._num_harmonics+1), self._f0, dtype=si_dtype_map[SI.F])

    def system_cmd(self, command, wait=True, dir_=None):
        command = command if isinstance(command, str) else " ".join(command)
        sep = " && " if sys.platform == "win32" else " ; "
        env = "%ENV%" if sys.platform == "win32" else "$ENV"
        dir_ = self.root if dir_ is None else dir_
        commands = (env, "cd %s" % (dir_,), command)
        process = Popen(sep.join(commands), shell=True, stdout=sys.stdout)
        if wait:
            process.wait()
        return process
