from sknrf.settings import Settings
from sknrf.model.sequencer.sweep.real import SpanSweep
from sknrf.utilities.numeric import Info, Scale
from sknrf.utilities.patterns import export


class AbstractFundSpanSweep(SpanSweep):
    """ Abstract Fundamental Span Sweep

        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        center : float, default 0.0
            Center value.
        span : float, default 0.0
            Span value.
        step : float, default 0.0
            Step value.
        points : int, default 0
            Number of points in the sweep.
        level : bool, default False
            Level the frequency sweep with a 1/sinc(t) filter.
    """
    display_order = ["realtime", "center", "span", "step", "points", "filter", "all"]

    def __new__(cls, realtime: bool = False,
                center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                level: bool = False, all_: bool = False):
        self = super(AbstractFundSpanSweep, cls).__new__(cls, realtime=realtime,
                                                         center=center, span=span, step=step, points=points)
        self.center = 0.0
        self.span = Settings().ss_span / Settings().t_step if span == 0.0 else span
        self._filter = level
        self._all = all_
        return self

    def __getnewargs__(self):
        new_args = list(super(AbstractFundSpanSweep, self).__getnewargs__())
        opt_args = [self.level, self.all]
        return tuple(new_args + opt_args)

    def __init__(self, realtime: bool = False,
                 center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                 level: bool = False, all_: bool = False):
        super(AbstractFundSpanSweep, self).__init__(realtime=realtime,
                                                    center=center, span=span, step=step, points=points)

        self.center = 0.0
        self.span = Settings().ss_span / Settings().t_step if span == 0.0 else span
        self.points = Settings().ss_points if points == 0 else points
        self.level = level
        self.all = all_

    def __info__(self):
        super(AbstractFundSpanSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["filter"] = Info("filter", read=True, write=True, check=True)
        self.info["all"] = Info("all", read=True, write=True, check=True)
        self.info["center"].scale, self.info["center"].unit = Scale.M, "Hz"
        self.info["center"].min, self.info["center"].max = 0.0, 0.0
        self.info["span"].scale, self.info["span"].unit = Scale.M, "Hz"
        self.info["span"].min, self.info["span"].max = 0.0, 1/Settings().t_step
        self.info["points"].min, self.info["points"].max = 2, Settings().t_points
        self.info["step"].scale, self.info["step"].unit = Scale.M, "Hz"
        self.info["step"].min, self.info["step"].max = 1/Settings().t_stop, 1e100

    def __getstate__(self, state={}):
        state = super(AbstractFundSpanSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(AbstractFundSpanSweep, self).__setstate__(state)

    @property
    def level(self):
        """ (float) Sweep filter value.
        """
        return self._filter

    @level.setter
    def level(self, filter_):
        self._level = filter_

    @property
    def all(self):
        """ (float) Apply all frequencies at once.
        """
        return self._all

    @all.setter
    def all(self, all_):
        self._all = all_


class FundLOSpanSweep(AbstractFundSpanSweep):
    """ Fundamental Local Oscillator (LO) Span Sweep

        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        center : float, default 0.0
            Center value.
        span : float, default 0.0
            Span value.
        step : float, default 1.0
            Step value.
        points : int, default 0
            Number of points in the sweep.
        level : bool, default False
            Level the frequency sweep with a 1/sinc(t) filter.
    """
    display_order = ["realtime", "center", "span", "step", "filter", "all"]

    def __new__(cls, realtime: bool = False,
                center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                level: bool = False, all_: bool = False):
        self = super(FundLOSpanSweep, cls).__new__(cls, realtime=realtime,
                                                   center=center, span=span, step=step, points=points,
                                                   level=level, all_=all_)
        return self

    @export
    def __init__(self, realtime: bool = False,
                 center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                 level: bool = False, all_: bool = False):
        super(FundLOSpanSweep, self).__init__(realtime=realtime,
                                              center=center, span=span, step=step, points=points,
                                              level=level, all_=all_)

        self.__info__()

    def __info__(self):
        super(FundLOSpanSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["filter"].write = False
        self.info["all"].write = False
        self.info["realtime"].write = False

    def __getstate__(self, state={}):
        state = super(FundLOSpanSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(FundLOSpanSweep, self).__setstate__(state)

    @property
    def filter(self):
        return self._level

    @filter.setter
    def level(self, filter_):
        self._level = True

    @property
    def all(self):
        return self._all

    @all.setter
    def all(self, all_):
        self._all = False


class FundPhasorSpanSweep(AbstractFundSpanSweep):
    """Fundamental Phasor Span Sweep

        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        center : float, default 0.0
            Center value.
        span : float, default 0.0
            Span value.
        step : float, default 1.0
            Step value.
        points : int, default 0
            Number of points in the sweep.
        level : bool, default False
            Level the frequency sweep with a 1/sinc(t) filter.
    """
    display_order = ["realtime", "center", "span", "step", "level", "all"]

    def __new__(cls, realtime: bool = False,
                center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                level: bool = False, all_: bool = False):
        self = super(FundPhasorSpanSweep, cls).__new__(cls, realtime=realtime,
                                                       center=center, span=span, step=step, points=points,
                                                       level=level, all_=all_)
        return self

    @export
    def __init__(self, realtime: bool = False,
                 center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                 level: bool = False, all_: bool = False):
        super(FundPhasorSpanSweep, self).__init__(realtime=realtime,
                                                  center=center, span=span, step=step, points=points,
                                                  level=level, all_=all_)

        self.__info__()

    def __info__(self):
        super(FundPhasorSpanSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        df = 1 / Settings().t_stop
        self.info["span"].min, self.info["span"].max = -1 / Settings().t_step + df, 1 / Settings().t_step - df
        self.info["points"].max = Settings().t_points - 2

    def __getstate__(self, state={}):
        state = super(FundPhasorSpanSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(FundPhasorSpanSweep, self).__setstate__(state)


class FundDSBSpanSweep(AbstractFundSpanSweep):
    """Fundamental Double Side-band (DSB) Span Sweep

        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        center : float, default 0.0
            Center value.
        span : float, default 0.0
            Span value.
        step : float, default 1.0
            Step value.
        points : int, default 0
            Number of points in the sweep.
        level : bool, default False
            Level the frequency sweep with a 1/sinc(t) filter.
    """
    display_order = ["realtime", "center", "span", "step", "level", "all"]

    def __new__(cls, realtime: bool = False,
                center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                level: bool = False, all_: bool = False):
        self = super(FundDSBSpanSweep, cls).__new__(cls, realtime=realtime,
                                                    center=center, span=span, step=step, points=points,
                                                    level=level, all_=all_)
        return self

    @export
    def __init__(self, realtime: bool = False,
                 center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                 level: bool = False, all_: bool = False):
        super(FundDSBSpanSweep, self).__init__(realtime=realtime,
                                               center=center, span=span, step=step, points=points,
                                               level=level, all_=all_)

        self.__info__()

    def __info__(self):
        super(FundDSBSpanSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["span"].min, self.info["span"].max = -1/(2*Settings().t_step), 1/(2*Settings().t_step)
        self.info["points"].max = Settings().t_points

    def __getstate__(self, state={}):
        state = super(FundDSBSpanSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(FundDSBSpanSweep, self).__setstate__(state)


class FundSSBSpanSweep(AbstractFundSpanSweep):
    """Fundamental Single Side-band (SSB) Span Sweep

        When points=0, step is used to specify the number of points.

        Parameters
        ----------
        center : float, default 0.0
            Center value.
        span : float, default 0.0
            Span value.
        step : float, default 1.0
            Step value.
        points : int, default 0
            Number of points in the sweep.
    """
    display_order = ["realtime", "center", "span", "step", "level", "all"]

    def __new__(cls, realtime: bool = False,
                center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                level: bool = False, all_: bool = False):
        self = super(FundSSBSpanSweep, cls).__new__(cls, realtime=realtime,
                                                    center=center, span=span, step=step, points=points,
                                                    level=level, all_=all_)
        return self

    @export
    def __init__(self, realtime: bool = False,
                 center: float = 0.0, span: float = 0.0, step: float = 1.0, points: int = 0,
                 level: bool = False, all_: bool = False):
        super(FundSSBSpanSweep, self).__init__(realtime=realtime,
                                               center=center, span=span, step=step, points=points,
                                               level=level, all_=all_)
        self.__info__()

    def __info__(self):
        super(FundSSBSpanSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        df = 1 / Settings().t_stop
        self.info["span"].min, self.info["span"].max = -1/Settings().t_step + df, 1/Settings().t_step - df
        self.info["points"].max = Settings().t_points - 2

    def __getstate__(self, state={}):
        state = super(FundSSBSpanSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(FundSSBSpanSweep, self).__setstate__(state)

