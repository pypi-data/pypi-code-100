# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tykes']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'pygame>=2.0.2,<3.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['tykes = tykes.cli:app']}

setup_kwargs = {
    'name': 'tykes',
    'version': '0.1.0',
    'description': 'A python project designed to provide low-stimulation games to young children.',
    'long_description': None,
    'author': 'Ian Wernecke',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
