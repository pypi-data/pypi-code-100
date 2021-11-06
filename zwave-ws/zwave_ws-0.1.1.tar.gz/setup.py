# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zwave_ws']

package_data = \
{'': ['*']}

install_requires = \
['websocket-client>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'zwave-ws',
    'version': '0.1.1',
    'description': 'Library, implementing websocket connection to ZWave-Me',
    'long_description': None,
    'author': 'Dmitry Vlasov',
    'author_email': 'kerbalspacema@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
