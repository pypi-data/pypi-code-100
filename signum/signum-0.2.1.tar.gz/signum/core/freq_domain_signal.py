from signum.core.base_container import SignalContainer, SCA


class BaseFreqDomainSignal(SignalContainer):
    ATTRIBUTES = SignalContainer.ATTRIBUTES + [SCA('_f_resolution', 1, True)]

    # alias for the property
    f_resolution = SignalContainer.resolution

    def __new__(cls, *args, f_resolution: float=None, **kwargs):
        obj = super().__new__(cls, *args, **kwargs, x_unit='Hz', x_description='Frequency')

        if f_resolution is not None:
            obj.f_resolution = f_resolution  # using the property setter

        return obj

    @property
    def resolution(self):
        return self._base_resolution * self._f_resolution

    @resolution.setter
    def resolution(self, val):
        self._resolution_setter_(val)

    def _resolution_setter_(self, val):
        self._f_resolution = val
        self._resolution_defaults_setter()

    @property
    def f_sampling(self):
        return self.resolution

    @f_sampling.setter
    def f_sampling(self, val):
        self._resolution_setter_(val)


