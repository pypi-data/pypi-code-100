# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wpilib_ws']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'wpilib-ws-py',
    'version': '0.1.2',
    'description': 'An implementation of the WPILib WebSocket protocol for Python',
    'long_description': '# wpilib-ws-py\n## An implementation of the WPILib WebSocket protocol for Python3\n\nThis library is an implementation of the WPILib simulation WebSocket, used for controlling non-frc hardware using WPILib. The specification of this protocol is found [here](https://github.com/wpilibsuite/allwpilib/blob/main/simulation/halsim_ws_core/doc/hardware_ws_api.md).\n\n[Example Sever Usage](tests/examples/demo_server.py)',
    'author': 'Patrick Brennan (AM2i9)',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AM2i9/wpilib-ws-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
