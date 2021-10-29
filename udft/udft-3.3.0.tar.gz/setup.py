# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udft']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.2,<2.0.0']

extras_require = \
{'fftw': ['pyFFTW>=0.12.0,<0.13.0']}

setup_kwargs = {
    'name': 'udft',
    'version': '3.3.0',
    'description': 'Unitary discrete Fourier Transform (and related)',
    'long_description': '# UDFT: Unitary Discrete Fourier Transform (and related)\n\n![licence](https://img.shields.io/github/license/forieux/udft) ![pypi](https://img.shields.io/pypi/v/udft) ![status](https://img.shields.io/pypi/status/udft) ![version](https://img.shields.io/pypi/pyversions/udft) ![maintained](https://img.shields.io/maintenance/yes/2021) [![Documentation Status](https://readthedocs.org/projects/udft/badge/?version=latest)](https://udft.readthedocs.io/en/latest/?badge=latest)\n\nThis module implements unitary discrete Fourier transform, that is orthonormal.\nThis module existed before the introduction of the `norm="ortho"` keyword and is\nnow a very (very) thin wrapper around Numpy or\n[pyFFTW](https://pypi.org/project/pyFFTW/) (maybe others in the future), mainly\ndone for my personal usage. There is also functions related to Fourier and\nconvolution like `ir2fr`.\n\nIt is useful for convolution [1]: they respect the Perceval equality, e.g., the\nvalue of the null frequency is equal to `1/√N * ∑ₙ xₙ`.\n\n```\n[1] B. R. Hunt "A matrix theory proof of the discrete convolution theorem", IEEE\nTrans. on Audio and Electroacoustics, vol. au-19, no. 4, pp. 285-288, dec. 1971\n```\n\nIf you are having issues, please let me know\n\nfrancois.orieux AT l2s.centralesupelec.fr\n\n## Installation and documentation\n\nUDFT is just the file `udft.py` and depends on `numpy` and Python 3.7+ only.\nDocumentation is [here](https://udft.readthedocs.io/en/stable/index.html). I\nrecommend using poetry for installation\n\n```\n   poetry add udft\n```\nor\n```\n   poetry add udft[fftw]\n```\nto install the [pyFFTW](https://pypi.org/project/pyFFTW/) also, but the package is available with pip also. For a quick and dirty installation, just copy the `udft.py` file: it is\nquite stable, follow the [Semantic\nVersioning](https://semver.org/spec/v2.0.0.html), and major changes are\nunlikely.\n\nThe code is hosted on [GitHub](https://github.com/forieux/udft).\n\n## License\n\nThe code is in the public domain.\n',
    'author': 'François Orieux',
    'author_email': 'francois.orieux@universite-paris-saclay.fr',
    'maintainer': 'François Orieux',
    'maintainer_email': 'francois.orieux@universite-paris-saclay.fr',
    'url': 'https://udft.readthedocs.io/en/stable/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
