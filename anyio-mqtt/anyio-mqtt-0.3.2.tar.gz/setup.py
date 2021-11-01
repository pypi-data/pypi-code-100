# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anyio_mqtt']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.1.0,<4.0.0', 'paho-mqtt>=1.5.1,<2.0.0', 'tenacity>=7.0.0,<8.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'anyio-mqtt',
    'version': '0.3.2',
    'description': 'Very early work in progress of an AnyIO MQTT client',
    'long_description': "This is just a very early-stage work in progress of an AnyIO MQTT client. It'd probably be best if you don't use it right now.\n\nPlease see https://github.com/sbtinstruments/asyncio-mqtt/discussions/44 to discuss the porting of an existing MQTT client to AnyIO.\n",
    'author': 'Ellis Percival',
    'author_email': 'anyio-mqtt@failcode.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
