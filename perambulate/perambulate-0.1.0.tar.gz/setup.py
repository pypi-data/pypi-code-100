# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perambulate', 'perambulate.condition']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0', 'numpy==1.18.1', 'pandas==1.0.1']

setup_kwargs = {
    'name': 'perambulate',
    'version': '0.1.0',
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
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
