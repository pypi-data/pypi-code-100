# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opendiamond', 'opendiamond.console']

package_data = \
{'': ['*']}

install_requires = \
['M2Crypto>=0.21.1',
 'click-plugins>=1.1.1,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'python-dateutil>=1.5']

entry_points = \
{'console_scripts': ['cookiecutter = '
                     'opendiamond.console.scope_generate:generate',
                     'diamond-newscope = '
                     'opendiamond.console.scope_import:import_',
                     'opendiamond-scope = opendiamond.console.scope:cli'],
 'opendiamond.cli_plugins': ['scope = opendiamond.console.scope:cli']}

setup_kwargs = {
    'name': 'opendiamond-scope',
    'version': '10.1.3',
    'description': 'OpenDiamond scope manipulation library and tools',
    'long_description': '# Opendiamond-scope\n\nLibrary and tools for manipulating OpenDiamond search scopes.\n\n\n# Building from source\n\nBuild depends on SWIG and OpenSSL to build the M2Crypto wheels.\n\n    sudo apt install swig libssl-dev\n\n    poetry install\n    poetry run opendiamond-scope -h\n',
    'author': 'Carnegie Mellon University',
    'author_email': 'diamond@cs.cmu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://diamond.cs.cmu.edu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
