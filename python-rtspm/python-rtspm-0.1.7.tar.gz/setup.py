# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtspm']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.8.1,<5.0.0', 'numpy>=1.19.2', 'scipy>=1.5.4']

setup_kwargs = {
    'name': 'python-rtspm',
    'version': '0.1.7',
    'description': 'Python adaptation of SPM functions for real-time fMRI analysis',
    'long_description': '# python-rtspm\nSPM functions in Python for real-time fMRI\n',
    'author': 'OpenNFT Team',
    'author_email': 'opennft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4',
}
from buildext import *
build(setup_kwargs)

setup(**setup_kwargs)
