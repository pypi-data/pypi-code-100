"""
    ==========
    Real Sweep
    ==========

    Real Number Parametric Sweep Plans.

    Example
    -------
    measure1 = measure.Measure()
    sweep1 = sweep.LinearSweep(realtime=False)

    measure1.add_sweep(sweep1, 'A', 1, 1, realtime=False)
    measure1.swept_measurement()

    See Also
    ----------
    sknrf.desktop.sequencer.measure

"""

from enum import Enum

import math as mt
import torch as th
from scipy.interpolate import interp1d

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.model.sequencer.sweep.base import AbstractSweep
from sknrf.utilities.numeric import Info, PkAvg, Format
from sknrf.utilities.numeric import factors
from sknrf.utilities.patterns import export


class INDEP_DIM(Enum):
    TIME = 0
    FREQ = 1


class LinearSweep(AbstractSweep):
    """ Real Linear Sweep Plan.

        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        start : float, default 0.0
            Start value.
        stop : float, default 1.0
            Stop value.
        step : float, default 0.1
            Step value.
        points : int, default 0
            Number of points in the sweep.
    """
    display_order = ["start", "stop", "points", "step", "realtime"]

    def __new__(cls, realtime: bool = False,
                start: float = 0.0, stop: float = 1.0, step: float = 0.1, points: int = 0):
        self = super(LinearSweep, cls).__new__(cls, realtime=realtime)

        self.start = start
        self.stop = stop
        self._points = points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.start, self.stop, self.step, self._points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 start: float = 0.0, stop: float = 1.0, step: float = 0.1, points: int=0):
        super().__init__(realtime=realtime)

        self.start = start
        self.stop = stop
        self._points = 2

        self.__info__()

        # Initialize object PROPERTIES
        if points:
            self.points = points
        else:
            self.step = step

    def __info__(self):
        super(LinearSweep, self).__info__()
        span = mt.fabs(self.stop - self.start)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["start"] = Info("start", write=True, check=True, unit="U", format_=Format.RE,
                                  min_=self.start - span/2., max_=self.stop + span/2)
        self.info["stop"] = Info("stop", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=self.start - span/2., max_=self.stop + span/2)
        self.info["step"] = Info("step", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=0.0, max_=span/1.99)
        self.info["points"] = Info("points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(LinearSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(LinearSweep, self).__setstate__(state)

    @property
    def step(self):
        return (self.stop - self.start)/(self._points - 1)

    @step.setter
    def step(self, step):
        assert(step != 0)
        self.points = mt.floor((self.stop - self.start)/step + 1)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = max(2, int(points))

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return th.linspace(self.start, self.stop, self._points, dtype=th.double)


class SpanSweep(AbstractSweep):
    """ Span Sweep
    
        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        center : float, default 0.0
            Center value.
        span : float, default 1.0
            Span value.
        step : float, default 0.1
            Step value.
        points : int, default 0
            Number of points in the sweep.
    """
    display_order = ["center", "span", "step", "realtime"]

    def __new__(cls, realtime: bool = False,
                center: float = 0.0, span: float = 1.0, step: float = 0.1, points: int = 0):
        self = super(SpanSweep, cls).__new__(cls, realtime=realtime)

        self.center = center
        self.span = span
        self._points = points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.center, self.span, self.step, self.points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 center: float = 0.0, span: float = 1.0, step: float = 0.1, points: int = 0):
        super().__init__(realtime=realtime)

        self.center = center
        self.span = span
        self._points = 2

        self.__info__()

        # Initialize object PROPERTIES
        if points:
            self.points = points
        else:
            self.step = step

    def __info__(self):
        super(SpanSweep, self).__info__()
        span = self.span
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["center"] = Info("center", write=True, check=True, unit="U", format_=Format.RE,
                                   min_=self.center - span/2., max_=self.center + span/2)
        self.info["span"] = Info("span", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=0.0, max_=self.span + span/2)
        self.info["step"] = Info("step", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=0.0, max_=span/1.99)
        self.info["points"] = Info("points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(SpanSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(SpanSweep, self).__setstate__(state)

    @property
    def step(self):
        return self.span/(self._points - 1)

    @step.setter
    def step(self, step):
        assert (step != 0)
        self.points = mt.floor(self.span/step + 1)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = max(2, int(points))

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return th.linspace(-self.span/2, self.span/2, self._points, dtype=th.double) + self.center


class SubsetSweep(AbstractSweep):
    """ Subset Sweep Plan.

        Subset a factor of the independent dim points.

        Parameters
        ----------
        dim : INDEP_DIM, default INDEP_DIM.TIME
            Independent dim
        step : int, default 1
            Step value.
        points : int, default 0
            Number of points in the sweep.
    """
    display_order = ["points", "step"]

    def __new__(cls, realtime: bool = False,
                dim: INDEP_DIM = INDEP_DIM.TIME, step: int = 1, points: int = 0):
        self = super(SubsetSweep, cls).__new__(cls, realtime=realtime)

        self._dim = dim
        self._points = points
        self.__interp = None
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self._dim, self.step, self._points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 dim: INDEP_DIM = INDEP_DIM.TIME, step: int = 1, points: int = 0):
        super().__init__(realtime=realtime)

        self._dim = INDEP_DIM.TIME
        self._points = 2

        self.__info__()

        # Initialize object PROPERTIES
        self.dim = dim
        if points:
            self.points = points
        else:
            self.step = step

    def __info__(self):
        super(SubsetSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["dim"] = Info("dim", read=True, write=True, check=True)
        self.info["step"] = Info("step", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=1, max_=self._dim_points())
        self.info["points"] = Info("points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(SubsetSweep, self).__getstate__(state=state)
        del state["_SubsetSweep__interp"]
        return state

    def __setstate__(self, state):
        super(SubsetSweep, self).__setstate__(state)

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, dim):
        self._dim = dim
        dim_points = self._dim_points()
        factor_array = th.as_tensor(list(factors(dim_points)), dtype=th.int)
        self.__interp = interp1d(factor_array, factor_array, kind="nearest")
        self.step = 1

    @property
    def step(self):
        return self._dim_points() / self._points

    @step.setter
    def step(self, step):
        self._points = max(int(self.__interp(self._dim_points() / step)), 2)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self.step = self._dim_points() / max(int(points), 2)

    def _dim_points(self):
        if self.dim == INDEP_DIM.TIME:
            return Settings().t_points
        else:
            return Settings().f_points

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return th.linspace(0, self.points, self.points, dtype=th.double)


class PowSweep(AbstractSweep):
    """ Real Power Sweep Plan.

        Parameters
        ----------
        start : float, default 0.0
            Start value.
        stop : float, default 1.0
            Stop value.
        points : int, default 11
            Number of points in the sweep.
        power : float, default 2
            Exponential power of the sweep.
    """
    display_order = ["start", "stop", "power", "points"]

    def __new__(cls, realtime: bool = False,
                start: float = 0.0, stop: float = 1.0, points: int = 11, power: float = 2.0):
        self = super(PowSweep, cls).__new__(cls, realtime=realtime)

        self.start = start
        self.stop = stop
        self._power = power
        self._points = points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.start, self.stop, self._points, self._power]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 start: float = 0.0, stop: float = 1.0, points: int = 11, power: float = 2.0):
        super().__init__(realtime=realtime)

        self.start = start
        self.stop = stop
        self._power = power
        self._points = points

        self.__info__()

        # Initialize object PROPERTIES
        self.power = power
        self.points = points

    def __info__(self):
        super(PowSweep, self).__info__()
        span = mt.fabs(self.stop - self.start)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["start"] = Info("start", write=True, check=True, unit="U", format_=Format.RE,
                                  min_=si_eps_map[SI.V], max_=self.stop + span/2)
        self.info["stop"] = Info("stop", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=si_eps_map[SI.V], max_=self.stop + span/2)
        self.info["power"] = Info("power", write=True, check=True,
                                  min_=0.001, max_=20)
        self.info["points"] = Info("points", write=True, check=True, min_=2)

    def __getstate__(self, state={}):
        state = super(PowSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(PowSweep, self).__setstate__(state)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, power):
        self._power = power

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = max(2, int(points))

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return th.linspace(self.start**self._power, self.stop**self._power, self._points, dtype=th.double)**(1/self._power)


class LogSweep(AbstractSweep):
    """ Real Logarithmic Sweep Plan.

        Parameters
        ----------
        start : float, default 1.0e-3
            Start value.
        stop : float, default 1.0
            Stop value.
        points : int, default 11
            Number of points in the sweep.
        base : float, default 10
            Logarithmic base of the sweep.
    """
    display_order = ["start", "stop", "base", "points"]

    def __new__(cls, realtime: bool = False,
                start: float = 1.0e-3, stop: float = 1.0, points: int = 11, base: float = 10.0):
        self = super(LogSweep, cls).__new__(cls, realtime=realtime)

        self.start = start
        self.stop = stop
        self._base = base
        self._points = points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.start, self.stop, self._points, self._base]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 start: float = 1.0e-3, stop: float = 1.0, points: int = 11, base: float = 10.0):
        super().__init__(realtime=realtime)

        self.start = start
        self.stop = stop
        self._base = base
        self._points = points

        self.__info__()

        # Initialize object PROPERTIES
        self.base = base
        self.points = points

    def __info__(self):
        super(LogSweep, self).__info__()
        span = mt.fabs(self.stop - self.start)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["start"] = Info("start", write=True, check=True, unit="U", format_=Format.LOG_DEG,
                                  min_=si_eps_map[SI.V], max_=self.stop + span/2)
        self.info["stop"] = Info("stop", write=True, check=True, unit="U", format_=Format.LOG_DEG,
                                 min_=si_eps_map[SI.V], max_=self.stop + span/2)
        self.info["base"] = Info("base", write=True, check=True,
                                  min_=0.001, max_=20)
        self.info["points"] = Info("points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(LogSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(LogSweep, self).__setstate__(state)

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, base):
        self._base = base

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = max(2, int(points))

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return th.logspace(mt.log10(self.start), mt.log10(self.stop), self._points, self._base, dtype=th.double)

