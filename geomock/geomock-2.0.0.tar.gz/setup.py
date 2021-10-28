# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geomock']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'numpy>=1.21.2,<2.0.0',
 'shapely-geojson>=0.0.1,<0.0.2',
 'toolz>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['geomock = geomock.cli:cli']}

setup_kwargs = {
    'name': 'geomock',
    'version': '2.0.0',
    'description': "'",
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
