# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['badexperiment']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'google-api-python-client',
 'google-auth-oauthlib',
 'pandas',
 'pyyaml']

entry_points = \
{'console_scripts': ['becli = badexperiment.becli:make_iot_yaml']}

setup_kwargs = {
    'name': 'badexperiment',
    'version': '0.1.17',
    'description': 'see https://github.com/turbomam/badexperiment',
    'long_description': None,
    'author': 'Mark A. Miller',
    'author_email': 'mamillerpa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
