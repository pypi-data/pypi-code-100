import logging

import numpy as np
from matplotlib import mlab

from signum.core.freq_domain_signal import BaseFreqDomainSignal as BaseFreqDomainSignal
from signum.core.time_domain_signal import BaseTimeDomainSignal as BaseTimeDomainSignal
from signum.tools.scale_manager import ScaleManager

logger = logging.getLogger(__name__)


class TimeDomainSignal(BaseTimeDomainSignal):
    def csd(self, other=None, **kwargs):
        """Cross spectral density"""

        if other is None:
            description = f"{self.description}: power spectral density"
            meta = {**self.meta, 'original_description': self.description}
            other = self

        else:
            # check that the operation is applicable to the inputs
            self.check_metadata(self, other, require_type=True)

            description = f"{self.description} & {other.description}: cross spectral density"
            meta = {**self.meta, **other.meta, 'original_descriptions': [self.description, other.description]}

        # calculate the spectrum
        spectrum, frequencies = mlab.csd(other, self, **kwargs, Fs=self.f_sampling)

        spectrum = FreqDomainSignal(spectrum, f_resolution=frequencies[1] - frequencies[0], x_start=frequencies[0],
                                    description=description, meta=meta, unit=self.unit)

        return spectrum

    def psd(self, **kwargs):
        """Power spectral density"""

        return self.csd(other=None, **kwargs)

    def fft(self, axis=-1, description='', **kwargs):
        self._check_x_axis_spacing("a Fourier transform")

        f = np.fft.fft(self, axis=axis, **kwargs)

        ns = self.shape[axis]
        f_resolution = self.f_sampling/ns
        description = description or (f"FFT of {self.description}" if self.description else '')

        f = FreqDomainSignal(f, f_resolution=f_resolution, description=description, meta=self.meta, unit=self.unit)

        return f


class FreqDomainSignal(BaseFreqDomainSignal):
    def ifft(self, axis=-1, description='', **kwargs):
        self._check_x_axis_spacing("an inverse Fourier transform")

        ns = self.shape[axis]
        f_sampling = self.f_resolution * ns
        description = description or (f"Inverse FFT of {self.description}" if self.description else '')

        if self.x_axis[0]:
            logger.warning(f"The first element of the array appears not to be the zero-frequency term (based on the "
                           f"frequency axis: {ScaleManager.display(self.x_axis[0], 'Hz')})")

        t = np.fft.ifft(self, axis=axis, **kwargs)
        t = TimeDomainSignal(t, meta=self.meta, unit=self.unit, description=description, f_sampling=f_sampling)
        return t

    def fftshift(self):
        self._check_x_axis_spacing("FFT shift")

        f = FreqDomainSignal(np.fft.fftshift(self))
        f.copy_attributes(self)
        f.x_start = self.x_start - self.x_axis[self.shape[-1] // 2]

        return f

    def ifftshift(self):
        self._check_x_axis_spacing("Inverse FFT shift")

        f = FreqDomainSignal(np.fft.ifftshift(self))
        f.copy_attributes(self)
        f.x_start = self.x_axis[self.shape[-1] // 2]

        return f


if __name__ == '__main__':
    # time domain
    tdata1 = TimeDomainSignal(np.random.rand(12), f_sampling=40e6, description='Signal 1')
    tdata2 = TimeDomainSignal(np.arange(12).reshape(1, -1), f_sampling=1, unit='V', description='Signal 2')
    tdata3 = TimeDomainSignal(np.arange(12), f_sampling=40e6, description='Signal 3')

    tdata1.display()

    psd = tdata1.psd()
    psd.display()

    csd = tdata1.csd(tdata3)
    csd.display()

    # freq domain
    fdata1 = FreqDomainSignal(np.random.rand(12) + 1j * np.random.rand(12), f_resolution=10, unit='mV',
                              description="Frequency response")
    fdata2 = FreqDomainSignal(np.arange(12).reshape(1, -1), unit='V', description="H")

    fdata2.reshape(-1).display()
    fdata1.display()
    fdata1.display(plot_type='bode', db_scale=True)
    fdata1.display(plot_type='nyquist')
