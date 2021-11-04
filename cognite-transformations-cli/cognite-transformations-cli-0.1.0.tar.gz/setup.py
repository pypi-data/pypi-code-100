# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite',
 'cognite.transformations_cli',
 'cognite.transformations_cli.commands',
 'cognite.transformations_cli.commands.deploy']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'cognite-extractor-utils>=1.5.2,<2.0.0',
 'cognite-sdk-experimental==0.60.22',
 'sqlparse>=0.4.2,<0.5.0',
 'tabulate>=0.8.9,<0.9.0',
 'types-retry>=0.1.5,<0.2.0',
 'types-tabulate>=0.8.3,<0.9.0']

entry_points = \
{'console_scripts': ['transformations_cli = '
                     'cognite.transformations_cli.__main__:main']}

setup_kwargs = {
    'name': 'cognite-transformations-cli',
    'version': '0.1.0',
    'description': 'A CLI for the Transformations service in CDF',
    'long_description': '# Transformations CLI\n\nThe Transormations CLI is a replacement for [jetfire-cli](https://github.com/cognitedata/jetfire-cli) rewritten on top\nof the new Python SDK for Transformations.\n\n\n',
    'author': 'Mathias Lohne',
    'author_email': 'mathias.lohne@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cognitedata/transformations-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
