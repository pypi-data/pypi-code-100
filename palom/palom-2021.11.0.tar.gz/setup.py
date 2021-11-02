# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['palom']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2021.10.0,<2022.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'napari-lazy-openslide>=0.2.0,<0.3.0',
 'numpy>=1.21.3,<2.0.0',
 'opencv-python>=4.5.3.56,<5.0.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.7.1,<2.0.0',
 'tifffile>=2021.10.12,<2022.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'zarr>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'palom',
    'version': '2021.11.0',
    'description': 'Piecewise alignment for layers of mosaics',
    'long_description': '# Piecewise alignment for layers of mosaics',
    'author': 'Yu-An Chen',
    'author_email': 'atwood12@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<3.8',
}


setup(**setup_kwargs)
