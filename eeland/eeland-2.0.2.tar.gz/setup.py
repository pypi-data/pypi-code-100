# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eeland']

package_data = \
{'': ['*']}

install_requires = \
['eland>=7.10.1-beta.1,<8.0.0']

entry_points = \
{'console_scripts': ['eeland = eeland.main:run_cli']}

setup_kwargs = {
    'name': 'eeland',
    'version': '2.0.2',
    'description': 'easy eland: cli&utils to make eland even easier to use',
    'long_description': None,
    'author': 'Federico Falconieri',
    'author_email': 'federico.falconieri@tno.nl',
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
