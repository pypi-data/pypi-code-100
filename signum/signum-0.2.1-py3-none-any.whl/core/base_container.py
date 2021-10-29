# based on: https://www.numpy.org/devdocs/user/basics.subclassing.html

import logging
from collections import abc
from numbers import Number
from typing import Iterable, List, NamedTuple, Any

import numpy as np

from signum.plotting import plot_signal

logger = logging.getLogger(__name__)

SCA = NamedTuple('DataContainerAttribute', [('name', str), ('default_value', Any), ('is_core', bool)])


class SignalContainer(np.ndarray):
    """A subclass of numpy.ndarray, wrapping array data to include metadata envelope (such as sampling frequency)."""

    ATTRIBUTES = [SCA('unit', '', True),
                  SCA('x_unit', '', True),
                  SCA('_base_resolution', 1, True),
                  SCA('x_start', 0, False),
                  SCA('_nonstandard_x_axis', None, False),
                  SCA('description', '', False),
                  SCA('x_description', '', False),
                  SCA('meta', {}, False)]

    def __new__(cls, data, unit: str = None, x_unit: str = None, description: str = None, x_description: str = None,
                x_start: float = None, x_axis=None, resolution: float = None, meta: dict = None):
        """Create a new instance of a SignalContainer.

        Parameters
        ----------
        data            :   array_like
            input data to be converted to an array (see numpy.asarray for more details)
        unit            :   str, optional
            data unit
        x_unit          :   str, optional
            unit of the x axis data (e.g. 's', 'Hz')
        description     :   str, optional
            data description
        x_description   :   str, optional
            description of the x axis data (e.g. 'Time')
        x_start         :   float, optional
            starting value for an automatically-generated x axis (calculated from data length and resolution)
        x_axis          :   array_like, optional
            nonstandard x axis data (e.g. if the signal data is not equally spaced); must match the first dimension
            of the data shape
        resolution      :   float, optional
            data spacing (in the x axis units)
        meta            :   dict, optional
            additional, user-provided metadata
        """

        obj = np.asarray(data).view(cls)

        def gv(val, name):
            return val if val is not None else getattr(obj, name)

        # definition of object properties
        obj.unit = gv(unit, 'unit')
        obj.x_unit = gv(x_unit, 'x_unit')
        obj.description = gv(description, 'description')
        obj.x_description = gv(x_description, 'x_description')
        obj.x_start = gv(x_start, 'x_start')
        obj.resolution = gv(resolution, 'resolution')  # using the resolution setter
        obj.meta = gv(meta, 'meta')

        if x_axis is not None:
            obj.x_axis = x_axis  # using the (nonstandard) x axis setter

        return obj

    def __array_finalize__(self, obj):
        """Finalize DataContainer instance creation by assigning the envelope attributes.

        This method is automatically called in every case a new instance of DataContainer is created (unlike __new__ and
        __init_, used only during explicit constructor call; in that case, __array_finalize__ is called first).
        See https://www.numpy.org/devdocs/user/basics.subclassing.html for more details.

        The goal of using this method is to make sure that all the envelope attributes are defined for the newly created
        object."""

        # update the attributes of the newly created object
        self._update_from_obj(obj)

    def _update_from_obj(self, obj=None):
        """Update self to include all the envelope attributes. Copy values from the template object or use defaults.

        The attribute values can come from three sources, depending on the way an instance is created:
        - class defaults (self.defaults from self.ATTRIBUTES)
        - previously defined values (self.__dict__)
        - template object (obj, instance of the same class as self).
        """

        # create container for attributes to be set
        _attributes = {}

        # pre-fill with default values; make sure all attribute names are present
        _attributes.update(self.defaults)

        # preserve current attribute values
        # (if present; when initializing from explicit constructor call, self.__dict__ at this point is empty)
        _attributes.update(self.__dict__)

        # copy attributes from obj (if it is of the same type as self; it might also be None)
        if isinstance(obj, type(self)):
            _attributes.update({k: getattr(obj, k) for k in _attributes.keys()})

        # update the instance attributes with the final set
        self.__dict__.update(_attributes)

    def toarray(self):
        return self.view(np.ndarray)

    @property
    def defaults(self):
        """Return a dictionary of the default values for the envelope attributes."""

        return {t.name: t.default_value for t in self.ATTRIBUTES}

    @property
    def core_attributes(self) -> List[str]:
        """Return a list of names of the core envelope attributes.

        These are the attributes that need to be taken into account when performing an operation (e.g. addition) on two
        DataContainers (their values must be the same for both inputs - otherwise the operation is not valid).
        """

        return [t.name for t in self.ATTRIBUTES if t.is_core]

    @property
    def envelope_attributes(self):
        """Return a dictionary of current values of the core envelope attributes."""

        return self.get_attributes(self.core_attributes)

    @property
    def envelope_attributes_extended(self):
        """Return a dictionary of current values of the core envelope attributes."""

        return self.get_attributes(self.defaults.keys())

    def get_attributes(self, attr_names: Iterable[str]):
        return {attr: getattr(self, attr, None) for attr in attr_names}

    @envelope_attributes.setter
    def envelope_attributes(self, envelope_dict):
        self.set_attributes(envelope_dict)

    def set_attributes(self, attributes_dict):
        invalid_keys = set(attributes_dict.keys()) - set(self.defaults.keys())
        n = len(invalid_keys)
        if n:
            raise AttributeError(f"{type(self)} has no attribute{'s' if n > 1 else ''}: {invalid_keys}")

        for k, v in attributes_dict.items():
            setattr(self, k, v)

    def copy_attributes(self, other):
        if not isinstance(other, type(self)):
            logger.warning(f"The template object is not an instance of {self.__class__.__name__}")
            return

        self._update_from_obj(other)

    @staticmethod
    def recast_type(func):
        """Perform view casting and copy attributes from the first input to first output of the decorated function."""

        def wrapper(data_in: SignalContainer, *args, **kwargs):
            data_out = func(data_in, *args, **kwargs)

            # if there are multiple outputs - handle only the first one, leave the rest unchanged
            if isinstance(data_out, tuple):
                data_out, *other_outputs = data_out
            else:
                other_outputs = ()

            # view casting
            data_out = data_out.view(type(data_in))

            # propagating attributes
            if isinstance(data_out, SignalContainer):
                data_out.copy_attributes(data_in)

            # fold the outputs tuple back
            return (data_out, *other_outputs) if other_outputs else data_out

        return wrapper

    def __array_ufunc__(self, ufunc, method, *args, **kwargs):

        args_envelope = []

        def check_envelope_attributes(obj, side="Inputs"):
            new_envelope = obj.envelope_attributes
            if not len(args_envelope):
                args_envelope.append(new_envelope)
            else:
                if args_envelope[0] != new_envelope:
                    raise TypeError(f"{side} attributes mismatch! ({args_envelope[0]}, {new_envelope})")

        inputs = []
        for arg in args:
            if isinstance(arg, self.__class__):
                check_envelope_attributes(arg)
                inputs.append(arg.view(np.ndarray))  # cast to plain ndarray
            else:
                inputs.append(arg)

        outputs = kwargs.pop('out', None)
        if outputs:
            out_args = []
            for output in outputs:
                if isinstance(output, self.__class__):
                    check_envelope_attributes(output, 'Input/output')
                    out_args.append(output.view(np.ndarray))
                else:
                    out_args.append(output)
            kwargs['out'] = tuple(out_args)
        else:
            outputs = (None,) * ufunc.nout

        results = super(SignalContainer, self).__array_ufunc__(ufunc, method, *inputs, **kwargs)

        if results is NotImplemented:
            return NotImplemented

        if ufunc.nout == 1:
            results = (results,)

        results_converted = []
        for result, output in zip(results, outputs):
            out = result if output is None else output

            if isinstance(out, Number):
                rconv = out
            else:
                # convert back to DataContainer
                rconv = np.asarray(out).view(self.__class__)
                rconv.copy_attributes(self)
            results_converted.append(rconv)

        return results_converted[0] if len(results_converted) == 1 else tuple(results_converted)

    def __getitem__(self, item):
        res = super().__getitem__(item)

        if isinstance(res, type(self)):
            if isinstance(item, (Number, slice, np.ndarray)):
                item = (item, )

            if isinstance(item, tuple):
                item = item[(self.ndim - self.x_axis.ndim):]

            res._nonstandard_x_axis = self.x_axis[item]  # nonstandard choice of indices

        return res

    @property
    def resolution(self):
        return self._base_resolution

    @resolution.setter
    def resolution(self, val):
        logger.debug(f"Setting base resolution to {val}")
        self._base_resolution = val

    def _resolution_defaults_setter(self):
        self._base_resolution = 1

    @property
    def x_axis(self):
        if self._nonstandard_x_axis is not None:
            return self._nonstandard_x_axis

        x0 = self.x_start if self.x_start is not None else 0
        return x0 + np.arange(self.shape[-1]) * self.resolution

    @x_axis.setter
    def x_axis(self, val):
        if val is None:
            return

        if not isinstance(val, (abc.Sequence, abc.Iterable)):
            raise TypeError("x axis should be a sequence")

        if not len(val) == self.shape[-1]:
            raise ValueError(f"Length of the x axis ({len(val)}) does not match the signal shape ({self.shape})")

        self._nonstandard_x_axis = np.array(val)

        if val is not None:
            self.x_start = 0

    @property
    def magnitude(self):
        mag = np.abs(self)
        mag.description = (self.description or '') + f' (magnitude)'
        return mag

    @property
    def magnitude_db(self):
        mag_db = 20 * np.log10(np.abs(self))  # TODO: dB for power quantities
        mag_db.unit = 'dB'
        mag_db.description = (self.description or '') + f'(magnitude, dB)'
        return mag_db

    @property
    def phase(self):
        return self.get_phase()

    def get_phase(self, rad=False, unwrapped=True):
        """Calculate phase of the signal.

        Parameters
        ----------
        rad         :   bool
            if True, return the phase in radians; otherwise (default) - use degrees
        unwrapped   :   bool
            if True (default), unwrap the phase to avoid 2pi jumps; otherwise, return the phase limited to (-pi, pi)
            or (-180, 180), depending on the desired unit
        """

        ph = np.angle(self)  # phase in radians

        if unwrapped:
            ph = np.unwrap(ph)
        if not rad:
            ph = np.rad2deg(ph)

        ph = ph.view(self.__class__)
        ph.copy_attributes(self)
        ph.unit = 'rad' if rad else 'deg'
        ph.description = (ph.description or '') + ' (phase)'
        return ph

    def display(self, plot_type: str = None, show: bool = False, title: str = None, **kwargs):
        """Create a plot to display the data.

        Parameters
        ----------
        plot_type   :   str
            type of plot to be created. Available options: 'bode' (default for complex-valued data), 'nyquist', 'iq',
             'polar', 'simple' (valid for real-valued data only).
        show        :   bool
            if True, display the plot; setting to False allows later customisation before displaying it
        title       :   str
            title for the plot; if not provided, the description of the signal is used
        kwargs
            additional keyword arguments passed to the specific plotting methods (or matplotlib.pyplot.plot)
        """

        if self.size < 2:
            kwargs['marker'] = kwargs.get('marker', 'o')  # put a single dot if there is only one data point

        plot_kwargs = {}

        for arg in ('unwrapped', 'db_scale', 'rad', 'figsize', 'sharey'):
            if arg in kwargs:
                plot_kwargs[arg] = kwargs.pop(arg)

        plotter = plot_signal(self, plot_type=plot_type, show=show, title=title, plot_kwargs=plot_kwargs, **kwargs)
        return plotter

    def _check_x_axis_spacing(self, label='requested operation'):
        if self._nonstandard_x_axis is not None:
            u = np.unique(np.diff(self._nonstandard_x_axis))
            m = np.median(u)
            tolerance = 10 * np.finfo(u.dtype).resolution

            if (np.abs(u - m) > tolerance).any():
                raise ValueError(f"Cannot perform {label} on an array of non-equally spaced samples")

