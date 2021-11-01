# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perambulate', 'perambulate.condition']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0', 'numpy', 'pandas>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'perambulate',
    'version': '0.1.3',
    'description': 'Timeseries analysis modules',
    'long_description': '',
    'author': 'Jordi Dekker',
    'author_email': 'pypi@jordidekker.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
