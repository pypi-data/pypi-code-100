import abc

import torch as th
from torch.nn import Module
from numpy.linalg import cond

from sknrf.settings import Settings, InstrumentFlag
from sknrf.model.base import AbstractModel
from sknrf.enums.signal import transform_color_map
from sknrf.utilities.numeric import Info, Scale, PkAvg, Format, Domain
from sknrf.utilities.error import nrmse, stde
__author__ = 'dtbespal'


# Instrument Reference Plane
# ---------------------------------------------------------
# fs(RF): RFVectorCal                    -> Cascade Transform
# fs(RFRECEIVER): RFAmplitudeCal         -> Cascade Transform
# fs(RFRECEIVER): RFPhaseCal             -> Cascade Transform
# fs(RFSOURCE): RFSourceCal              -> Cascade Transform
# es(LFSOURCE): PortSourceDelayCal         -> Delay Transform    (Not Done)
# es(SOURCE): SourceDelayCal             -> Delay Transform
# es(RECEIVER): ReceiverDelayCal         -> Delay Transform
# es(All): PhaseNormalizationCal         -> Custom Phase Normalization
# es(LFSource or RFSource): ETDelayCal   -> Delay Transform    (Not Done)
# ps(LFSource): ETShapingCal             -> Shaping Transform
# ps(RFSource): DPDCal                   -> DPD Transform
# ---------------------------------------------------------
# DUT Reference Plane
#
# Notes:
# ET Delay needs to delay RFSource if LFSource does not have the timing resolution
#
# Not yet implemented:
#  - es: IQDelayCal (Source)
#    - Determines the delay between I and Q inside the Source
#  - es: IQGainCal (Source)
#    - Determines the gain between I and Q inside the Source
#  - es: IQCarrierDelayCal (Source)
#    - Determines the delay between the IQ modulator and the carrier signal


class GoodnessOfFit(AbstractModel):
    """ Goodness of Fit

    Stores the goodness of fit of a behavioural model.

    Attributes
    ----------
    cond : tensor
        Condition number of the problem matrix.
    nrmse : bool
        Normalized Root-Mean-Square Error.
    """

    def __new__(cls, ports=(1,)):
        self = super(GoodnessOfFit, cls).__new__(cls)
        return self

    @abc.abstractmethod
    def __getnewargs__(self):
        return tuple(self.ports)

    def __init__(self, ports=(1,)):
        """ Goodness of fit

        Parameters
        ----------
        ports : tuple
            The ports that apply the goodness of fit.
        """
        super(GoodnessOfFit, self).__init__()
        self.ports = ports
        shape = (len(self.ports), Settings().f_points)

        self.cond = th.ones(shape, dtype=th.double)
        self.nrmse = th.ones(shape, dtype=th.double)
        self.stde = th.ones(shape, dtype=th.double)

        self.__info__()

    @abc.abstractmethod
    def __getstate__(self, state={}):
        state = super(GoodnessOfFit, self).__getstate__(state=state)
        return state

    @abc.abstractmethod
    def __setstate__(self, state):
        super(GoodnessOfFit, self).__setstate__(state=state)

    @abc.abstractmethod
    def __info__(self):
        super(GoodnessOfFit, self).__info__()
        self.info["ports"] = Info("ports", read=False, write=False, check=False)
        self.info["cond"] = Info("cond", read=True, write=False, check=True, min_=1, scale=Scale._)
        self.info["nrmse"] = Info("NRMSE", read=True, write=False, check=True, min_=0, max_=1, scale=Scale._,
                                  format_=Format.LOG_DEG)
        self.info["stde"] = Info("std(error)", read=True, write=False, check=True, min_=0, max_=1, scale=Scale.m,
                                 format_=Format.RE)

    def calculate(self, A, x_, y):
        """ Calculate the goodness of fit.

        Parameters
        ----------
        A : tensor
            MxN problem matrix.
        x_ : tensor
            NX1 expected input data
        y : tensor
            1XM  actual output data
        """
        y_ = th.matmul(A, x_)
        self.cond = cond(A)
        self.nrmse = nrmse(y_, y)
        self.stde = stde(y_, y)


class AbstractTransform(Module, AbstractModel):
    """ Abstract Transform

    Attributes
    ----------
    display_order : list[str]
        Display order of Attributes.
    optimize : bool
        Optimization flag.
    """
    _num_ports = -1
    _domain = Domain.TF
    _device = "cpu"
    _preview_filename = ":/PNG/unknown_circuit_transform.png"
    _default_filename = ""
    _color_code = Settings().color_map[transform_color_map[Domain.TF]]
    display_order = ["name", "ports"]
    optimize = True
    training: bool = True

    @abc.abstractmethod
    def __new__(cls, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL):
        self = super(AbstractTransform, cls).__new__(cls)

        self.name = name
        self._ports = list(ports)
        self._filename = ""
        self._file = None
        self._instrument_flags = instrument_flags
        self._data_ = None
        if not self.instrument_flags:
            raise AttributeError("At least one instrument flag must be raised")
        Module.__init__(self)
        return self

    def __getnewargs__(self):
        return self.name, self.ports, self.instrument_flags

    @abc.abstractmethod
    def __init__(self, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL):
        """ Abstract Transform

        Parameters
        ----------
        name : str
            Sweep name.
        ports : tuple [int]
            ports that apply the transform.
        instrument_flags : InstrumentFlag
            instruments that apply the transform.
        """
        AbstractModel.__init__(self)
        if self.__class__ == AbstractTransform:
            self.__info__()

    def release(self):
        pass

    def __getstate__(self, state={}):
        state["_filename"] = self._filename
        return state

    def __setstate__(self, state):
        self._filename = state["_filename"]

    def __info__(self):
        super(AbstractTransform, self).__info__()
        self.info["name"] = Info("name", read=True, write=True, check=True)
        self.info["ports"] = Info("ports", write=True, max_=Settings().num_ports, check=True)
        self.info["file"] = Info("file", read=False, write=False, check=False)
        self.info["instrument_flags"] = Info("instrument_flags", read=True, write=True, check=True)
        self.info["optimize"] = Info("optimize", read=False, write=False, check=False)
        self.info["training"] = Info("training", read=False, write=False, check=False)
        self.info["dump_patches"] = Info("dump patches", read=False, write=False, check=False)

    def color(self):
        """The color code assigned to the transform.

        Returns
        -------
        str
            A color code."""
        return self._color_code

    @property
    def ports(self):
        """Tuple[int]: Ports that apply the transform"""
        return self._ports

    @ports.setter
    def ports(self, ports):
        if len(set(ports)) != self._num_ports:
            raise ValueError("%s is a %d-Port Transform" % (self.__class__.__name__, self._num_ports))
        elif max(ports) > Settings().num_ports:
            raise ValueError("Ports entry exceeds the maximum number of ports: %d " % Settings().num_ports)
        else:
            self._ports = ports

    @property
    def instrument_flags(self):
        """Instrument: Instruments that apply the transform"""
        return self._instrument_flags

    @instrument_flags.setter
    def instrument_flags(self, instrument_flags):
        self._instrument_flags = instrument_flags


class _BehavioralModel(AbstractTransform):
    """ Behavioral Model

    Mixin class that includes Behavioural modelling parameters.

    Attributes
    ----------
    n : list[list[int]]
        Nonlinear Order for each port/harmonic.
    n_mix : list[list[int]]
        Nonlinear Mixing Order for each port/harmonic.
    m : list[list[int]]
        Memory Order for each port/harmonic.
    m_mix : list[list[int]]
        Memory Mixing Order for each port/harmonic.
    m_mix : list[list[int]]
        Memory Mixing Order for each port/harmonic.
    train_dg: str
        Training datagroup name.
    train_ds: str
        Training dataset name.
    train_fit: GoodnessOfFit
        Training goodness of fit.
    val_dg: str
        Validation datagroup name.
    val_ds: str
        Validation dataset name.
    val_fit: GoodnessOfFit
        Validation goodness of fit.
    """

    def __new__(cls, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL,
                data: th.Tensor = None,
                coeffs: th.Tensor = th.tensor([[1.0]]), coeffs_inv: th.Tensor = th.tensor([[1.0]])):
        self = super(_BehavioralModel, cls).__new__(cls, name, ports, instrument_flags=instrument_flags)
        self._data_ = data

        self.n = [1]*len(self.ports)
        self.n_mix = [1]*len(self.ports)
        self.m = [1]*len(self.ports)
        self.m_mix = [1]*len(self.ports)

        self.train_dg = "DPD"
        self.train_ds = "Train"
        self.train_fit = GoodnessOfFit(self.ports)
        self.val_dg = "DPD"
        self.val_ds = "Validate"
        self.val_fit = GoodnessOfFit(self.ports)

        self._coeffs = coeffs
        self._coeffs_inv = coeffs_inv
        return self

    def __getnewargs__(self):
        state = super(_BehavioralModel, self).__getnewargs__()
        state = tuple(list(state) +
                      [self._data_, self._coeffs, self._coeffs_inv])
        return state

    def __init__(self, name: str, ports: tuple, instrument_flags=InstrumentFlag.ALL,
                 data: th.Tensor = None,
                 coeffs: th.Tensor = th.tensor([[1.0]]), coeffs_inv: th.Tensor = th.tensor([[1.0]])):
        super(_BehavioralModel, self).__init__(name, ports, instrument_flags=instrument_flags)

    def __getstate__(self, state={}):
        super(_BehavioralModel, self).__getstate__(state=state)
        state["n"] = self.n
        state["n_mix"] = self.n_mix
        state["m"] = self.m
        state["m_mix"] = self.m_mix

        state["train_dg"] = self.train_dg
        state["train_ds"] = self.train_ds
        state["val_dg"] = self.val_dg
        state["val_ds"] = self.val_ds
        return state

    def __setstate__(self, state):
        super(_BehavioralModel, self).__setstate__(state=state)
        self.n = state["n"]
        self.n_mix = state["n_mix"]
        self.m = state["m"]
        self.m_mix = state["m_mix"]

        self.train_dg = state["train_dg"]
        self.train_ds = state["train_ds"]
        self.val_dg = state["val_dg"]
        self.val_ds = state["val_ds"]

    def __info__(self):
        super(_BehavioralModel, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["n"] = Info("n", read=False, write=False, check=False)
        self.info["n_mix"] = Info("n mix", read=False, write=False, check=False)
        self.info["m"] = Info("m", read=False, write=False, check=False)
        self.info["m_mix"] = Info("m mix", read=False, write=False, check=False)

        self.info["train_dg"] = Info("train datagroup", read=False, write=False, check=False)
        self.info["train_ds"] = Info("train dataset", read=False, write=False, check=False)
        self.info["train_fit"] = Info("train fit", read=False, write=False, check=False)
        self.info["val_dg"] = Info("val datagroup", read=False, write=False, check=False)
        self.info["val_ds"] = Info("val dataset", read=False, write=False, check=False)
        self.info["val_fit"] = Info("val fit", read=False, write=False, check=False)

    def train(self):
        """Calculate the training goodness of fit."""
        pass

    def validate(self):
        """Calculate the validation goodness of fit."""
        pass
