# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carto2gpd', 'carto2gpd.tests']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.10.1,<0.11.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'carto2gpd',
    'version': '1.0.11',
    'description': 'A Python utility to query a CARTO database and return a geopandas GeoDataFrame',
    'long_description': None,
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
