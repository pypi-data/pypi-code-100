# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['SibylSystem', 'SibylSystem.types']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'sibylsystem',
    'version': '0.0.2',
    'description': 'Python Wrapper for the Sibyl System Antispam API for telegram',
    'long_description': '# SibylPy\n\n## Python3 wrapper for the Sibyl System antispam API for telegram\n',
    'author': 'Sayan Biswas',
    'author_email': 'sayan@pokurt.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AnimeKaizoku/SibylSystem-Py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
