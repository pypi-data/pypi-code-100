# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['terramagic']
install_requires = \
['click>=8.0.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'pyfiglet>=0.8.post1,<0.9',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['terramagic = terramagic:main']}

setup_kwargs = {
    'name': 'terramagic',
    'version': '0.0.6',
    'description': 'A automate tool for terraform projects',
    'long_description': None,
    'author': 'Milton Jesus',
    'author_email': 'milton.lima@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
