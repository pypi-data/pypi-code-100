"""
    =====
    Sweep
    =====

    Parametric Sweep Plans.

    Example
    -------
    measure1 = measure.Measure()
    linear_sweep = sweep.LinearSweep()

    measure1.add_sweep("A_1_1", linear_sweep)
    measure1.swept_measurement()

    See Also
    ----------
    sknrf.desktop.sequencer.measure
"""

import abc

import torch as th

from sknrf.enums.runtime import SI, si_dtype_map
from sknrf.model.base import AbstractModel
from sknrf.utilities.numeric import Info
from sknrf.utilities.patterns import export

__author__ = 'dtbespal'


class AbstractSweep(AbstractModel):
    """ Abstract Sweep Class.

        Base class for all sweep types.
    """

    @abc.abstractmethod
    def __new__(cls, realtime=False):
        self = super(AbstractSweep, cls).__new__(cls)
        self._realtime = realtime
        self._coupled_set = {"time", "freq"}
        return self

    @abc.abstractmethod
    def __getnewargs__(self):
        return (self.realtime,)

    @abc.abstractmethod
    def __init__(self, realtime=False):
        super(AbstractSweep, self).__init__()
        self._realtime = realtime

    @abc.abstractmethod
    def __getstate__(self, state={}):
        state = super(AbstractSweep, self).__getstate__(state=state)
        return state

    @abc.abstractmethod
    def __setstate__(self, state):
        super(AbstractSweep, self).__setstate__(state)
        self._coupled_set = state["_coupled_set"]

    @abc.abstractmethod
    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        super(AbstractSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["realtime"] = Info("realtime", read=True, write=True, check=True)
        self.info["coupled_set"] = Info("coupled_set", read=False, write=False, check=False)

    @property
    def realtime(self):
        return self._realtime

    @realtime.setter
    def realtime(self, realtime):
        self._realtime = realtime

    @property
    def coupled_set(self):
        return self._coupled_set
    
    @export
    def add_coupled(self, coupled):
        self._coupled_set.add(coupled)

    @export
    def remove_coupled(self, coupled):
        self._coupled_set.discard(coupled)

    @abc.abstractmethod
    def values(self):
        """ The values of the sweep.

            Return:
                values (ndarray): An array of values in the sweep
        """
        return th.tensor([], dtype=si_dtype_map[SI.Z])
