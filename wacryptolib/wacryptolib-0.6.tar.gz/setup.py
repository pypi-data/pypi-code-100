# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wacryptolib']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'decorator>=4.4.2,<5.0.0',
 'jsonrpc-requests>=0.4.0,<0.5.0',
 'jsonschema>=4.1.2,<5.0.0',
 'multitimer>=0.3,<0.4',
 'pycryptodome>=3.9.9,<4.0.0',
 'pymongo>=3.11.2,<4.0.0',
 'pytz>=2020.5,<2021.0',
 'schema>=0.7.2,<0.8.0',
 'uuid0>=0.2.7,<0.3.0']

extras_require = \
{':sys_platform == "linux"': ['pyudev>=0.22.0,<0.23.0', 'psutil>=5.8.0,<6.0.0'],
 ':sys_platform == "win32"': ['wmi>=1.5.1,<2.0.0', 'pywin32>=300']}

setup_kwargs = {
    'name': 'wacryptolib',
    'version': '0.6',
    'description': 'Witness Angel Cryptolib',
    'long_description': "Witness Angel Cryptolib\n#############################\n\n.. image:: https://travis-ci.com/WitnessAngel/witness-angel-cryptolib.svg?branch=master\n    :target: https://travis-ci.com/WitnessAngel/witness-angel-cryptolib\n\n.. image:: https://readthedocs.org/projects/witness-angel-cryptolib/badge/?version=latest&style=flat\n    :target: https://witness-angel-cryptolib.readthedocs.io/en/latest/\n\n\n`Full documentation on readthedocs! <https://witness-angel-cryptolib.readthedocs.io/en/latest/>`_\n\n\nSummary\n----------------\n\n**WARNING, HUGE REFACTORING OF THIS LIB WILL SOON OCCUR**\n\nThis lib gathers utilities to generate and store cryptographic keys, and encrypt/decrypt/sign container, for the\nWitnessAngel project.\n\nIt defines a container format which allows multiple agents (the user's device as well as trusted-third-parties) to\nadd layers of encryption and signature to the sensitive data.\n\nIt also provides utilities for webservices and their error handling, as well as test-helpers so that software using\nthe library may easily check that their own subclasses respect the invariants of this system.\n\n\nCLI interface\n----------------\n\nYou can play with containers using this command line interface.\n\nbeware, unless you provide your own crypto-config, these CLI-generated containers will use a hard-coded and simple cryptographic conf, using only locally-stored keys, so they will be insecure.\n\n::\n\n    $ python -m wacryptolib encrypt -i <data-file> -o <container-file>\n\n    $ python -m wacryptolib decrypt -i <container-file> -o <data-file>\n",
    'author': 'Pascal Chambon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://witnessangel.com/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
