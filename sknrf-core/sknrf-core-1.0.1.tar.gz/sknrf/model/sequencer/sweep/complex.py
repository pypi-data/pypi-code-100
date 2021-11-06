"""
    =============
    Complex Sweep
    =============

    Complex Number Parametric Sweep Plans.
    
    Example
    -------
    measure1 = measure.Measure()
    sweep1 = sweep.RectangularSweep(realtime=False)
    
    measure1.add_sweep(sweep1, 'A', 1, 1, realtime=False)
    measure1.swept_measurement()
    
    See Also
    ----------
    sknrf.desktop.sequencer.measure

"""

import math as mt
import torch as th

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.model.sequencer.sweep.base import AbstractSweep
from sknrf.model.sequencer._shape import Coordinate, SHAPE, ShapeMap, Grid
from sknrf.utilities.numeric import Info, Format
from sknrf.utilities.patterns import export

__author__ = 'dtbespal'


class CustomSweep(AbstractSweep):
    """ Custom Sweep Plan.

        When points=0, step is used to specify the number of points.

    Parameters
    ----------
    values : Tensor
        Custom sweep plan values.
    """

    def __new__(cls, realtime: bool = False,
                values: th.Tensor = th.tensor([0.0])):
        self = super(CustomSweep, cls,).__new__(cls, realtime=realtime)
        self._values = values
        return self

    def __getnewargs__(self):
        new_args = list(super(CustomSweep, self).__getnewargs__())
        opt_args = [self._values]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 values=th.tensor([0.0])):
        super(CustomSweep, self).__init__(realtime=realtime)
        self.__info__()

        self._values = values

    def __getstate__(self, state={}):
        state = super(CustomSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(CustomSweep, self).__setstate__(state)
        self._values = state["_values"]

    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        super(CustomSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return self._values


class RectangularSweep(AbstractSweep):
    """ Complex Rectangular Linear Sweep Plan.

        When real_points=0, real_step is used to specify the number of points. When imag_points=0, imag_points is used
        to specify the number of points.

        Parameters
        ----------
        real_start : float, default -0.707
            Real start value.
        real_stop : float, default 0.707
            Real stop value.
        imag_start : float, default -0.707
            Imaginary start value.
        imag_stop : float, default 0.707
            Imaginary stop value.
        real_step : float, default 0.1414
            Real step value.
        real_points : int, default 0
            Number of real points in the sweep.
        imag_step : float, default 0.1414
            Imaginary step value.
        imag_points=0 : int, default 0
            Number of imag points in the sweep.
    """
    display_order = ["real_start", "real_stop", "imag_start", "imag_stop",
                     "real_points", "real_step", "imag_points", "imag_step"]

    def __new__(cls, realtime: bool = False,
                real_start: float = -0.707, real_stop: float = 0.707,
                imag_start: float = -0.707, imag_stop: float = 0.707,
                real_step: float = 0.1414, real_points: int = 0, imag_step: float = 0.1414, imag_points: int = 0):
        self = super(RectangularSweep, cls, ).__new__(cls, realtime=realtime)
        self.real_start = real_start
        self.real_stop = real_stop
        self._real_points = real_points
        self.imag_start = imag_start
        self.imag_stop = imag_stop
        self._imag_points = imag_points
        return self

    def __getnewargs__(self):
        new_args = list(super(RectangularSweep, self).__getnewargs__())
        opt_args = [self.real_start, self.real_stop,
                    self.imag_start, self.imag_stop,
                    self.real_step, self._real_points, self.imag_step, self._imag_points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 real_start: float = -0.707, real_stop: float = 0.707,
                 imag_start: float = -0.707, imag_stop: float = 0.707,
                 real_step: float = 0.1414, real_points: int = 0, imag_step: float = 0.1414, imag_points: int = 0):
        super().__init__(realtime=realtime)
        self.real_start = real_start
        self.real_stop = real_stop
        self._real_points = 2
        self.imag_start = imag_start
        self.imag_stop = imag_stop
        self._imag_points = 2

        self.__info__()

        # Initialize object PROPERTIES
        if real_points:
            self.real_points = real_points
        else:
            self.real_step = real_step
        if imag_points:
            self.imag_points = imag_points
        else:
            self.imag_step = imag_step

    def __info__(self):
        super(RectangularSweep, self).__info__()
        real_span = mt.fabs(self.real_stop - self.real_start)
        imag_span = mt.fabs(self.imag_stop - self.imag_start)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["real_start"] = Info("real_start", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.real_start - real_span/2., max_=self.real_stop + real_span/2.)
        self.info["real_stop"] = Info("real_stop", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.real_start - real_span/2., max_=self.real_stop + real_span/2.)
        self.info["real_step"] = Info("real_step", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=0.0, max_=real_span/1.99)
        self.info["real_points"] = Info("real_points", write=True,  min_=2, check=True)
        self.info["imag_start"] = Info("imag_start", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.imag_start - imag_span/2., max_=self.imag_stop + imag_span/2.)
        self.info["imag_stop"] = Info("imag_stop", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=self.imag_start - imag_span/2., max_=self.imag_stop + imag_span/2.)
        self.info["imag_step"] = Info("imag_step", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=0.0, max_=imag_span/1.99)
        self.info["imag_points"] = Info("imag_points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(RectangularSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(RectangularSweep, self).__setstate__(state)

    @property
    def real_step(self):
        return (self.real_stop - self.real_start)/(self._real_points - 1)

    @real_step.setter
    def real_step(self, real_step):
        assert(real_step != 0)
        self.real_points = mt.floor((self.real_stop - self.real_start)/real_step + 1)

    @property
    def real_points(self):
        return self._real_points

    @real_points.setter
    def real_points(self, real_points):
        self._real_points = max(2, int(real_points))

    @property
    def imag_step(self):
        return (self.imag_stop - self.imag_start) / (self._imag_points - 1)

    @imag_step.setter
    def imag_step(self, imag_step):
        assert(imag_step != 0)
        self.imag_points = mt.floor((self.imag_stop - self.imag_start) / imag_step + 1)

    @property
    def imag_points(self):
        return self._imag_points

    @imag_points.setter
    def imag_points(self, imag_points):
        self._imag_points = max(2, int(imag_points))

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        values = th.linspace(self.real_start, self.real_stop, self.real_points, dtype=th.double).reshape(-1, 1) + \
            th.linspace(self.imag_start, self.imag_stop, self.imag_points, dtype=th.double)*1j
        return values.flatten()


class PolarSweep(AbstractSweep):
    """ Complex Polar Linear Sweep Plan.

        When abs_points=0, abs_step is used to specify the number of points. When angle_points=0, angle_points is used
        to specify the number of points.

        Parameters
        ----------
        abs_start : float, default 0.0
            Amplitude start value.
        abs_stop : float, default 1.0
            Amplitude stop value.
        angle_start : float, default -180.0
            Angle start value.
        angle_stop : float, default 180.0
            Angle stop value.
        abs_step : float, default 0.1
            Amplitude step value.
        abs_points : int, default 0
            Number of amplitude points in the sweep.
        angle_step : float, default 60.0
            Angle step value.
        angle_points : int, default 0
            Number of angle points in the sweep
    """
    display_order = ["abs_start", "abs_stop", "abs_points", "abs_step",
                     "angle_start", "angle_stop", "angle_points", "angle_step"]

    def __new__(cls, realtime: bool = False,
                abs_start: float = 0.0, abs_stop: float = 1.0,
                angle_start: float = -180.0, angle_stop: float = 180.0,
                abs_step: float = 0.1, abs_points: int = 0, angle_step: float = 60.0, angle_points: int = 0):
        self = super(PolarSweep, cls,).__new__(cls, realtime=realtime)
        self.abs_start = abs_start
        self.abs_stop = abs_stop
        self._abs_points = abs_points
        self.angle_start = angle_start
        self.angle_stop = angle_stop
        self._angle_points = angle_points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.abs_start, self.abs_stop,
                    self.angle_start, self.angle_stop,
                    self.abs_step, self._abs_points, self.angle_step, self._angle_points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 abs_start: float = 0.0, abs_stop: float = 1.0,
                 angle_start: float = -180.0, angle_stop: float = 180.0,
                 abs_step: float = 0.1, abs_points: int = 0, angle_step: float = 60.0, angle_points: int = 0):
        super().__init__(realtime=realtime)
        # Initialize object ATTRIBUTES before self.__info__()
        self.abs_start = abs_start
        self.abs_stop = abs_stop
        self._abs_points = 2
        self.angle_start = angle_start
        self.angle_stop = angle_stop
        self._angle_points = 2

        self.__info__()

        # Initialize object PROPERTIES
        if abs_points:
            self.abs_points = abs_points
        else:
            self.abs_step = abs_step
        if angle_points:
            self.angle_points = angle_points
        else:
            self.angle_step = angle_step

    def __info__(self):
        super(PolarSweep, self).__info__()
        abs_stop = mt.fabs(self.abs_stop)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["abs_start"] = Info("abs_start", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=si_eps_map[SI.V], max_=self.abs_stop + abs_stop/2)
        self.info["abs_stop"] = Info("abs_stop", write=True, check=True, unit="U", format_=Format.RE,
                                     min_=si_eps_map[SI.V], max_=self.abs_stop + abs_stop/2)
        self.info["abs_step"] = Info("abs_step", write=True, check=True,
                                     min_=0.0, max_=(self.abs_stop + abs_stop/2)/2)
        self.info["abs_points"] = Info("abs_points", write=True,  min_=2, check=True)
        self.info["angle_start"] = Info("angle_start", write=True, check=True, unit="U", format_=Format.RE,
                                        min_=si_eps_map[SI.V], max_=360.)
        self.info["angle_stop"] = Info("angle_stop", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=si_eps_map[SI.V], max_=360.)
        self.info["angle_step"] = Info("angle_step", write=True, check=True,
                                       min_=0.0, max_=180.)
        self.info["angle_points"] = Info("angle_points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(PolarSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(PolarSweep, self).__setstate__(state)

    @property
    def abs_step(self):
        return (self.abs_stop - self.abs_start)/(self._abs_points - 1)

    @abs_step.setter
    def abs_step(self, abs_step):
        assert(abs_step != 0)
        self.abs_points = mt.floor((self.abs_stop - self.abs_start)/abs_step + 1)

    @property
    def abs_points(self):
        return self._abs_points

    @abs_points.setter
    def abs_points(self, abs_points):
        self._abs_points = max(2, int(abs_points))

    @property
    def angle_step(self):
        return (self.angle_stop - self.angle_start)/(self._angle_points - 1)

    @angle_step.setter
    def angle_step(self, angle_step):
        assert(angle_step != 0)
        self.angle_points = mt.floor((self.angle_stop - self.angle_start)/angle_step + 1)

    @property
    def angle_points(self):
        return self._angle_points

    @angle_points.setter
    def angle_points(self, angle_points):
        self._angle_points = max(2, int(angle_points))

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        values = th.linspace(self.abs_start, self.abs_stop, self.abs_points, dtype=th.double).reshape(-1, 1) * \
            th.exp(1j*mt.pi/180*th.linspace(self.angle_start, self.angle_stop, self.angle_points, dtype=th.double))
        return values.flatten()


class RectangularUniformSweep(AbstractSweep):
    """ Complex Rectangular Uniform Sweep Plan.

        Parameters
        ----------
        shape : SHAPE, default TRIANGLE
            Uniform grid shape.
        real_start : float, default -0.707
            Real start value.
        real_stop : float, default 0.707
            Real stop value.
        imag_start : float, default -0.707
            Imaginary start value.
        imag_stop : float, default 0.707
            Imaginary stop value.
        step : float, default 0.1414
            Uniform step value.
    """
    display_order = ["shape", "real_start", "real_stop",
                     "imag_start", "imag_stop", "step"]

    def __new__(cls, realtime: bool = False,
                shape: SHAPE = SHAPE.TRIANGLE, real_start: float = -0.707, real_stop: float = 0.707,
                imag_start: float = -0.707, imag_stop: float = 0.707, step: float = 0.1414):
        self = super(RectangularUniformSweep, cls,).__new__(cls, realtime=realtime)
        self.shape = shape
        self._shape_func = ShapeMap[shape]
        self.real_start = real_start
        self.real_stop = real_stop
        self.imag_start = imag_start
        self.imag_stop = imag_stop
        self._step = step
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.shape, self.real_start, self.real_stop,
                    self.imag_start, self.imag_stop, self._step]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 shape: SHAPE = SHAPE.TRIANGLE, real_start: float = -0.707, real_stop: float = 0.707,
                 imag_start: float = -0.707, imag_stop: float = 0.707, step: float = 0.1414):
        super().__init__(realtime=realtime)
        # Initialize object ATTRIBUTES before self.__info__()
        self.shape = shape
        self._shape_func = ShapeMap[shape]
        self.real_start = real_start
        self.real_stop = real_stop
        self.imag_start = imag_start
        self.imag_stop = imag_stop
        self._step = step

        self.__info__()

        # Initialize object PROPERTIES
        self.step = step

    def __info__(self):
        super(RectangularUniformSweep, self).__info__()
        real_span = mt.fabs(self.real_stop - self.real_start)
        imag_span = mt.fabs(self.imag_stop - self.imag_start)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["shape"] = Info("shape", write=True, check=True)
        self.info["real_start"] = Info("real_start", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.real_start - real_span/2., max_=self.real_stop + real_span/2.)
        self.info["real_stop"] = Info("real_stop", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.real_start - real_span/2., max_=self.real_stop + real_span/2.)
        self.info["real_step"] = Info("real_step", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=0.0, max_=real_span/1.99)
        self.info["real_points"] = Info("real_points", write=True,  min_=2, check=True)
        self.info["imag_start"] = Info("imag_start", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.imag_start - imag_span/2., max_=self.imag_stop + imag_span/2.)
        self.info["imag_stop"] = Info("imag_stop", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=self.imag_start - imag_span/2., max_=self.imag_stop + imag_span/2.)
        self.info["imag_step"] = Info("imag_step", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=0.0, max_=imag_span/1.99)
        self.info["imag_points"] = Info("imag_points", write=True,  min_=2, check=True)

    def __getstate__(self, state={}):
        state = super(RectangularUniformSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(RectangularUniformSweep, self).__setstate__(state)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        assert(step > 0)
        self._step = step

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        x_start, x_stop, y_start, y_stop = self.real_start, self.real_stop, self.imag_start, self.imag_stop

        #  Top Left, Bottom_Right in index coordinates
        i_start, j_stop = self._shape_func.world_to_vertex(Coordinate(x_start, y_stop), self.step)
        i_stop, j_start = self._shape_func.world_to_vertex(Coordinate(x_stop, y_start), self.step)
        points = (int(abs(i_stop - i_start)), int(abs(j_stop - j_start)))

        grid = Grid(self._shape_func, self.step)
        grid.add_face_array(list(range(0, points[0])), list(range(0, points[1])))
        vertices_ = set()
        for face_ in grid.faces:
            for corner_ in self._shape_func.corners(face_):
                vertices_.add(self._shape_func.vertex_to_world(corner_, self.step))
        if not vertices_:
            return th.tensor([], dtype=th.double)

        v_array = th.as_tensor(list(vertices_))
        x_offset = ((x_stop + x_start) - (v_array[:, 0].max() + v_array[:, 0].min()))/2
        y_offset = ((y_stop + y_start) - (v_array[:, 1].max() + v_array[:, 1].min()))/2
        v_array = (v_array[:, 0] + x_offset) + (v_array[:, 1] + y_offset) * 1j
        v_array = v_array[(x_start < v_array.real) & (v_array.real < x_stop) &
                          (y_start < v_array.imag) & (v_array.imag < y_stop)]
        return v_array


class PolarUniformSweep(AbstractSweep):
    """ Complex Polar Uniform Sweep Plan.

        Parameters
        ----------
        shape : SHAPE, default HEXAGON
            Uniform grid shape.
        abs_start : float, default 0.0
            Amplitude start value.
        abs_stop : float, default 1.0
            Amplitude stop value.
        step : float, default 0.1
            Uniform step value.
    """
    display_order = ["shape", "abs_start", "abs_stop", "step"]

    def __new__(cls, realtime: bool = False,
                shape=SHAPE.HEXAGON, abs_start: float = 0.0, abs_stop: float = 1.0, step: float = 0.1):
        self = super(PolarUniformSweep, cls,).__new__(cls, realtime=realtime)
        self.shape = shape
        self._shape_func = ShapeMap[shape]
        self.abs_start = abs_start
        self.abs_stop = abs_stop
        self._step = step
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self.shape, self.abs_start, self.abs_stop, self._step]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 shape=SHAPE.HEXAGON, abs_start: float = 0.0, abs_stop: float = 1.0, step: float = 0.1):
        super().__init__(realtime=realtime)
        # Initialize object ATTRIBUTES before self.__info__()
        self.shape = shape
        self._shape_func = ShapeMap[shape]
        self.abs_start = abs_start
        self.abs_stop = abs_stop
        self._step = step

        self.__info__()

        # Initialize object PROPERTIES
        self.step = step

    def __info__(self):
        super(PolarUniformSweep, self).__info__()

        abs_stop = mt.fabs(self.abs_stop)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["shape"] = Info("shape", write=True, check=True)
        self.info["abs_start"] = Info("abs_start", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=si_eps_map[SI.V], max_=self.abs_stop + abs_stop/2)
        self.info["abs_stop"] = Info("abs_stop", write=True, check=True, unit="U", format_=Format.RE,
                                     min_=si_eps_map[SI.V], max_=self.abs_stop + abs_stop/2)
        self.info["step"] = Info("step", write=True, check=True, unit="U", format_=Format.RE,
                                 min_=si_eps_map[SI.V], max_=self.abs_stop/1.99)

    def __getstate__(self, state={}):
        state = super(PolarUniformSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(PolarUniformSweep, self).__setstate__(state)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        assert(step > 0)
        self._step = step

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        x_start, x_stop, y_start, y_stop = (-self.abs_stop, self.abs_stop, -self.abs_stop, self.abs_stop)

        #  Top Left, Bottom_Right in index coordinates
        i_start, j_stop = self._shape_func.world_to_vertex(Coordinate(x_start, y_stop), self.step)
        i_stop, j_start = self._shape_func.world_to_vertex(Coordinate(x_stop, y_start), self.step)
        points = (int(abs(i_stop - i_start)), int(abs(j_stop - j_start)))

        grid = Grid(self._shape_func, self.step)
        grid.add_face_array(list(range(0, points[0]-1)), list(range(0, points[1]-1)))
        vertices_ = set()
        for face_ in grid.faces:
            for corner_ in self._shape_func.corners(face_):
                vertices_.add(self._shape_func.vertex_to_world(corner_, self.step))
        if not vertices_:
            return th.tensor([], dtype=th.double)

        v_array = th.as_tensor(list(vertices_))
        x_offset = ((x_stop + x_start) - (v_array[:, 0].max() + v_array[:, 0].min()))/2
        y_offset = ((y_stop + y_start) - (v_array[:, 1].max() + v_array[:, 1].min()))/2
        v_array = (v_array[:, 0] + x_offset) + (v_array[:, 1] + y_offset) * 1j
        v_array = v_array[(self.abs_start < v_array.abs()) & (v_array.abs() < self.abs_stop)]
        return v_array


class RectangularRandomSweep(AbstractSweep):
    """ Complex Rectangular Random Sweep Plan.

        Parameters
        ----------
        real_start : float, default -0.707
            Real start value.
        real_stop : float, default 0.707
            Real stop value.
        imag_start : float, default -0.707
            Imaginary start value.
        imag_stop : float, default 0.707
            Imaginary stop value.
        points : int, default 100
            Number of points in the sweep.
    """
    display_order = ["real_start", "real_stop",
                     "imag_start", "imag_stop", "points"]

    def __new__(cls, realtime: bool = False,
                real_start: float = -0.707, real_stop: float = 0.707,
                imag_start: float = -0.707, imag_stop: float = 0.707,
                points: int = 100):
        self = super(RectangularRandomSweep, cls,).__new__(cls, realtime=realtime)
        self._real_start = real_start
        self._real_stop = real_stop
        self._imag_start = imag_start
        self._imag_stop = imag_stop
        self._points = points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self._real_start, self._real_stop,
                    self._imag_start, self._imag_stop,
                    self._points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 real_start: float = -0.707, real_stop: float = 0.707,
                 imag_start: float = -0.707, imag_stop: float = 0.707,
                 points: int = 100):
        super().__init__(realtime=realtime)
        # Initialize object ATTRIBUTES before self.__info__()
        self._real_start = real_start
        self._real_stop = real_stop
        self._imag_start = imag_start
        self._imag_stop = imag_stop
        self._points = points
        self._values = self._randomize_values()

        self.__info__()

        # Initialize object PROPERTIES

    def __info__(self):
        super(RectangularRandomSweep, self).__info__()
        real_span = mt.fabs(self.real_stop - self.real_start)
        imag_span = mt.fabs(self.imag_stop - self.imag_start)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["real_start"] = Info("real_start", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.real_start - real_span/2., max_=self.real_stop + real_span/2.)
        self.info["real_stop"] = Info("real_stop", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=self.real_start - real_span/2., max_=self.real_stop + real_span/2.)
        self.info["imag_start"] = Info("imag_start", write=True, check=True, unit="U", format_=Format.RE,
                                       min_=self.imag_start - imag_span/2., max_=self.imag_stop + imag_span/2.)
        self.info["imag_stop"] = Info("imag_stop", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=self.imag_start - imag_span/2., max_=self.imag_stop + imag_span/2.)
        self.info["points"] = Info("points", write=True,  min_=1, max_=100, check=True)

    def __getstate__(self, state={}):
        state = super(RectangularRandomSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(RectangularRandomSweep, self).__setstate__(state)

    @property
    def real_start(self):
        return self._real_start

    @real_start.setter
    def real_start(self, real_start):
        self._real_start = real_start
        self._values = self._randomize_values()

    @property
    def real_stop(self):
        return self._real_stop

    @real_stop.setter
    def real_stop(self, real_stop):
        self._real_stop = real_stop
        self._values = self._randomize_values()

    @property
    def imag_start(self):
        return self._imag_start

    @imag_start.setter
    def imag_start(self, imag_start):
        self._imag_start = imag_start
        self._values = self._randomize_values()

    @property
    def imag_stop(self):
        return self._imag_stop

    @imag_stop.setter
    def imag_stop(self, imag_stop):
        self._imag_stop = imag_stop
        self._values = self._randomize_values()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        assert(points >= 1)
        self._points = points
        self._values = self._randomize_values()

    def _randomize_values(self):
        points = int(mt.sqrt(self.points))
        x_scale, x_offset = mt.fabs(self._real_stop - self._real_start), self._real_start
        y_scale, y_offset = mt.fabs(self._imag_stop - self._imag_start), self._imag_start
        values = (th.rand((points, points)) * th.tensor(x_scale) + th.tensor(x_offset)) \
               + (th.rand((points, points)) * th.tensor(y_scale) + th.tensor(y_offset)) * 1j
        return values

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return self._values


class PolarRandomSweep(AbstractSweep):
    """ Complex Polar Random Sweep Plan.

        Parameters
        ----------
        abs_start : float, default 0.0
            Amplitude start value.
        abs_stop : float, default 1.0
            Amplitude stop value.
        points : int, default 100
            Number of points in the sweep.
    """
    display_order = ["abs_start", "abs_stop", "points"]

    def __new__(cls, realtime: bool = False,
                abs_start: float = 0.0, abs_stop: float = 1.0, points: int = 100):
        self = super(PolarRandomSweep, cls,).__new__(cls, realtime=realtime)
        self._abs_start = abs_start
        self._abs_stop = abs_stop
        self._points = points
        return self

    def __getnewargs__(self):
        new_args = list(AbstractSweep.__getnewargs__(self))
        opt_args = [self._abs_start, self._abs_stop, self._points]
        return tuple(new_args + opt_args)

    @export
    def __init__(self, realtime: bool = False,
                 abs_start: float = 0.0, abs_stop: float = 1.0, points: int = 100):
        super().__init__(realtime=realtime)
        # Initialize object ATTRIBUTES before self.__info__()
        self._abs_start = abs_start
        self._abs_stop = abs_stop
        self._points = points
        self._values = self._randomize_values()

        self.__info__()
        # Initialize object PROPERTIES

    def __info__(self):
        super(PolarRandomSweep, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["abs_start"] = Info("abs_start", write=True, min_=0.0, check=True, unit="U", format_=Format.RE)
        self.info["abs_stop"] = Info("abs_stop", write=True, min_=1e-100, check=True, unit="U", format_=Format.RE)

        abs_stop = mt.fabs(self.abs_stop)
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["abs_start"] = Info("abs_start", write=True, check=True, unit="U", format_=Format.RE,
                                      min_=si_eps_map[SI.V], max_=self.abs_stop + abs_stop/2)
        self.info["abs_stop"] = Info("abs_stop", write=True, check=True, unit="U", format_=Format.RE,
                                     min_=si_eps_map[SI.V], max_=self.abs_stop + abs_stop/2)
        self.info["points"] = Info("points", write=True, min_=1, max_=100, check=True)

    def __getstate__(self, state={}):
        state = super(PolarRandomSweep, self).__getstate__(state=state)
        return state

    def __setstate__(self, state):
        super(PolarRandomSweep, self).__setstate__(state)

    @property
    def abs_start(self):
        return self._abs_start

    @abs_start.setter
    def abs_start(self, abs_start):
        self._abs_start = abs_start
        self._values = self._randomize_values()

    @property
    def abs_stop(self):
        return self._abs_stop

    @abs_stop.setter
    def abs_stop(self, abs_stop):
        self._abs_stop = abs_stop
        self._values = self._randomize_values()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        assert(points >= 1)
        self._points = points
        self._values = self._randomize_values()

    def _randomize_values(self):
        points = int(mt.sqrt(self.points))
        x_scale, x_offset = mt.fabs(self._abs_stop + self._abs_stop), -self._abs_stop
        y_scale, y_offset = mt.fabs(self._abs_stop + self._abs_stop), -self._abs_stop
        values = (th.rand((points, points)) * th.tensor(x_scale) + th.tensor(x_offset)) \
               + (th.rand((points, points)) * th.tensor(y_scale) + th.tensor(y_offset)) * 1j
        values = values[(self._abs_start < values.abs()) & (values.abs() < self._abs_stop)]
        return values

    def values(self):
        """ The values of the sweep.

        Returns
        -------
        values : Tensor
            The sweep plan values.
        """
        return self._values
