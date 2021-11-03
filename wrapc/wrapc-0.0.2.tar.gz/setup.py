# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wrapc']
install_requires = \
['argcomplete>=1.12.3,<2.0.0', 'argparse>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['wrapc = wrapc:main']}

setup_kwargs = {
    'name': 'wrapc',
    'version': '0.0.2',
    'description': 'Wrapper script for starting a command line tool with bash completion',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
