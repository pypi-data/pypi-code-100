# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obswebsocket_trio']

package_data = \
{'': ['*']}

install_requires = \
['single-source>=0.2.0,<0.3.0',
 'six>=1.16.0,<2.0.0',
 'trio-websocket>=0.9.2,<0.10.0',
 'trio>=0.19.0,<0.20.0',
 'typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'obswebsocket-trio',
    'version': '0.1.0',
    'description': 'Python library to communicate with an obs-websocket server, trio async version. Fork of obs-websocket-py<https://github.com/Elektordi/obs-websocket-py>',
    'long_description': None,
    'author': 'Michael D. M. Dryden',
    'author_email': 'mk.dryden@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
