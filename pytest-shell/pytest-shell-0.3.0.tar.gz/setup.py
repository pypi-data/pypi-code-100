# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_shell']

package_data = \
{'': ['*']}

install_requires = \
['where>=1.0.2,<2.0.0']

entry_points = \
{'pytest11': ['shell = pytest_shell']}

setup_kwargs = {
    'name': 'pytest-shell',
    'version': '0.3.0',
    'description': 'A pytest plugin to help with testing shell scripts / black box commands',
    'long_description': None,
    'author': 'Daniel Murray',
    'author_email': 'daniel@darkdisco.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
