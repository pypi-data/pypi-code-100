# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitre_attack',
 'mitre_attack.api',
 'mitre_attack.api.rest',
 'mitre_attack.cli',
 'mitre_attack.cli.command_groups',
 'mitre_attack.data',
 'mitre_attack.data.matrices',
 'mitre_attack.data.types']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'coverage[toml]>=6.1.1,<7.0.0',
 'hodgepodge>=2.3.2,<3.0.0',
 'setuptools>=58.5.3,<59.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['mitre-attack = mitre_attack.cli:cli',
                     'server = mitre_attack.api.rest.server:cli']}

setup_kwargs = {
    'name': 'mitre-attack',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tyler Fisher',
    'author_email': 'tylerfisher@tylerfisher.ca',
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
