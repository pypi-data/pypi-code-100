# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unicornhathd']

package_data = \
{'': ['*']}

install_requires = \
['Adafruit-Blinka>=6.15.0,<7.0.0',
 'adafruit-circuitpython-framebuf>=1.4.7,<2.0.0']

setup_kwargs = {
    'name': 'circuitpython-unicornhathd',
    'version': '0.6.0',
    'description': "CircuitPython framebuf based driver for Pimoroni's Unicorn HAT HD",
    'long_description': None,
    'author': 'Nathan Young',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
