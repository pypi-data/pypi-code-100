# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lobbyboy', 'lobbyboy.contrib', 'lobbyboy.contrib.provider']

package_data = \
{'': ['*'], 'lobbyboy': ['conf/*']}

install_requires = \
['paramiko[gssapi]>=2.8.0,<3.0.0',
 'python-digitalocean>=1.17.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['lobbyboy-config-example = '
                     'lobbyboy.utils:print_exmaple_config',
                     'lobbyboy-server = lobbyboy.server:main']}

setup_kwargs = {
    'name': 'lobbyboy',
    'version': '0.2.3',
    'description': 'Give me a server.',
    'long_description': None,
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
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
