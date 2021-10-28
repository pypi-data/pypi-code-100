# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkitekt',
 'arkitekt.actors',
 'arkitekt.agents',
 'arkitekt.agents.qt',
 'arkitekt.cli',
 'arkitekt.contracts',
 'arkitekt.graphql',
 'arkitekt.legacy',
 'arkitekt.messages',
 'arkitekt.messages.app',
 'arkitekt.messages.postman',
 'arkitekt.messages.postman.assign',
 'arkitekt.messages.postman.provide',
 'arkitekt.messages.postman.reserve',
 'arkitekt.messages.postman.unassign',
 'arkitekt.messages.postman.unprovide',
 'arkitekt.messages.postman.unreserve',
 'arkitekt.monitor',
 'arkitekt.packers',
 'arkitekt.packers.models',
 'arkitekt.packers.transpilers',
 'arkitekt.policies',
 'arkitekt.qt',
 'arkitekt.qt.images',
 'arkitekt.qt.port',
 'arkitekt.qt.widgets',
 'arkitekt.schema',
 'arkitekt.transport',
 'arkitekt.ui',
 'arkitekt.ui.qtwidgets']

package_data = \
{'': ['*'], 'arkitekt.qt.images': ['darkmode/*', 'lightmode/*']}

install_requires = \
['docstring-parser>=0.10,<0.11',
 'herre>=0.1.34,<0.2.0',
 'inflection>=0.5.1,<0.6.0',
 'janus>=0.6.1,<0.7.0',
 'websockets>=10.0,<11.0']

entry_points = \
{'console_scripts': ['arkitekt = arkitekt.cli.main:entrypoint']}

setup_kwargs = {
    'name': 'arkitekt',
    'version': '0.1.66',
    'description': 'rpc and node backbone',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
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
