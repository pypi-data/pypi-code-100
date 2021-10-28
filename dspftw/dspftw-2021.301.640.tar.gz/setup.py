# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dspftw']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.0,<2.0.0', 'scipy>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'dspftw',
    'version': '2021.301.640',
    'description': 'Starting points and helper functions for learning digital signal processing.',
    'long_description': '# DSPFTW\n\nStarting points and helper functions for learning digital signal processing.\n\n\n## Setup\n\nIf you haven\'t already, install Python 3.5 or greater, and the `dspftw` package.\n\n```sh\npython3 -m pip install dspftw --user\n```\n\n## Intro\n\n### Decomposition\n\n[Superposition: The foundation of DSP](http://www.dspguide.com/ch5/6.htm)\n\n### Sinusoids\nPrefer to use the complex exponential form instead of real, as it\'s a more natural fit for fourier analysis and synthesis.\n\nThe following functions represent a complex sinusoid.  They are equivalent, and take the same parameters:\n\n* A = Amplitude (y axis is amplitude).\n* f = Frequency (cycles per second) in Hertz.  It is multiplied by 2π to get radians per second.\n* t = Time in seconds.  These functions work in the time domain (x axis is time).\n* ϕ = Phase offset at t=0, in radians.\n\n```\nz(t) = A*exp(j*(2π*f*t+ϕ))\n\nz(t) = A*cos(2π*f*t+ϕ)+j*A*sin(2π*f*t+ϕ)\n```\n\nWe can define this in Python with the following.\n\n```python\nimport numpy as np\n\n# Here we use the name "complex_sinusoid" instead of just "z".\ndef complex_sinusoid(A, f, t, phi): return A * np.exp(1j*(2*np.pi*f*t+phi))\n```\n\nIn fact, this is defined in the `dspftw` package, so let\'s import that.\n\n```python\nimport dspftw\n```\n\nWe can create our own sinusoid by defining everything except `t`.\n\n```python\ndef my_sinusoid(t): return dspftw.complex_sinusoid(A=5, f=5, t=t, phi=0)\n```\n\nWe can get the signal at a bunch of times thanks to numpy arrays.  We use `numpy.linspace` to generate the evenly spaced times.\n\n```python\nimport numpy as np\ntimes = np.linspace(0, 1, num=25)  # 25 evenly spaced values between 0 and 1\nmy_signal = my_sinusoid(times)  # returns an array of complex values representing the signal\n```\n\nNow plot it out with `dspftw.plot_complex()`, which uses matplotlib.\n\n```python\nimport matplotlib.pyplot as plt\ndspftw.plot_complex(my_signal)\nplt.show()\n```\n\n[Complex Exponential Signals](https://www.cs.ccu.edu.tw/~wtchu/courses/2012s_DSP/Lectures/Lecture%203%20Complex%20Exponential%20Signals.pdf)\n\n### Roots of Unity\n![Roots of Unity Animation](https://mathworld.wolfram.com/images/gifs/rootsu.gif)\n\n[Wolfram Mathworld](https://mathworld.wolfram.com/RootofUnity.html)\n\n### Delta Function\n\n### Conjugate\n\n[Complex Conjugate](https://en.wikipedia.org/wiki/Complex_conjugate)\n\n### Convolution\n\n[Convolution](https://www.dspguide.com/ch6/2.htm)\n\n### Correlation\n\n[numpy.correlate](https://numpy.org/doc/stable/reference/generated/numpy.correlate.html)\n\n### Kronecker Product\n\n[numpy.kron](https://numpy.org/doc/stable/reference/generated/numpy.kron.html)\n\n### Sample Signals\n\n[SigIDWiki sample signals](https://www.sigidwiki.com/)\n\n### Loading Signals\n\n#### Complex 8 bit\n\n```python\nimport numpy as np\nsignal = np.fromfile(\'filename\', dtype=\'b\')  # load the whole file\nsignal = np.fromfile(\'filename\', dtype=\'b\', count=1024)  # only load the first 1024 bytes of the file\nsignal = np.fromfile(\'filename\', dtype=\'b\', offset=1024)  # skip the first 1024 bytes of the file\nsignal = np.fromfile(\'filename\', dtype=\'b\', offset=1024, count=1024)  # skip 1024, then load 1024\n```\n\nThis just loads the values as an array of real numbers, but we want it as complex.  We have to interpret every other value as the imaginary component.\n\n```python\nsignal = signal[0::2] + signal[1::2]*1j\n```\n\n#### Complex 32 bit float, little-endian (x86)\n\n```python\nsignal = np.fromfile(\'filename\', dtype=\'<f\')\n```\n\n`count` and `offset` work as above, but note that `offset` is in bytes, so you must multiple by 4 since there are 4 bytes in 32 bits.\n\n\n#### Complex 32 bit float, big-endian\n\n```python\nsignal = np.fromfile(\'filename\', dtype=\'>f\')\n```\n\n`count` and `offset` work as above, but note that `offset` is in bytes, so you must multiple by 4 since there are 4 bytes in 32 bits.\n',
    'author': 'Bill Allen',
    'author_email': 'billallen256@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/dspftw/dspftw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
