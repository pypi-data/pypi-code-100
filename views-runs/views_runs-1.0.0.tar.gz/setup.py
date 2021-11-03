# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_runs']

package_data = \
{'': ['*']}

install_requires = \
['sklearn>=0.0,<0.1',
 'stepshift>=2.0.0,<2.1.0',
 'views-partitioning>=2.3.0,<2.4.0']

setup_kwargs = {
    'name': 'views-runs',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
