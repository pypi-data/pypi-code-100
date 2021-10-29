import numpy as np
import logging

from signum.tools.scale_manager import ScaleManager
from signum.core.base_container import SignalContainer, SCA


logger = logging.getLogger(__name__)


class BaseTimeDomainSignal(SignalContainer):
    ATTRIBUTES = SignalContainer.ATTRIBUTES + [SCA('_t_sampling', 1, True)]

    def __new__(cls, *args, f_sampling: float = 1, f_sampling_unit='Hz', **kwargs):
        kwargs['x_unit'] = kwargs.pop('x_unit', 's')
        kwargs['x_description'] = kwargs.pop('x_description', 'Time')
        obj = super().__new__(cls, *args, **kwargs)

        # set sampling time
        f_sampling, f_sampling_unit = ScaleManager.rescale_to_basic(f_sampling, f_sampling_unit)
        obj.t_sampling = 1./f_sampling  # using the t sampling setter

        return obj

    @property
    def resolution(self):
        return self._base_resolution * self._t_sampling

    @resolution.setter
    def resolution(self, val):
        self._resolution_setter_(val)

    def _resolution_setter_(self, val):
        self._t_sampling = val
        self._resolution_defaults_setter()

    @property
    def t_sampling(self):
        return self.resolution

    @t_sampling.setter
    def t_sampling(self, val):
        self._resolution_setter_(val)

    @property
    def f_sampling(self):
        return 1./self.t_sampling

    @f_sampling.setter
    def f_sampling(self, val):
        self._resolution_setter_(1./val)

    @staticmethod
    def check_metadata(arr1, arr2, require_type=False):
        for i, arr in enumerate([arr1, arr2]):
            if not isinstance(arr, BaseTimeDomainSignal):
                m = f'Input array #{i+1} is not an instance of BaseTimeDomainSignal'
                if require_type:
                    raise TypeError(m)
                logger.debug(m)
                return

        if not np.isclose(arr1.f_sampling, arr2.f_sampling):
            raise ValueError(f"Inputs sampling frequencies mismatch: {arr1.f_sampling:.2E} and {arr2.f_sampling:.2E}")
