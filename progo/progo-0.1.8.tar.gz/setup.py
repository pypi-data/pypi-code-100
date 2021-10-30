# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['progo', 'progo.ble']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'bleak>=0.12.1,<0.13.0',
 'construct>=2.10.67,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.21.2,<2.0.0',
 'opencv-python>=4.5.3,<5.0.0',
 'packaging>=21.2,<22.0',
 'requests>=2.26.0,<3.0.0',
 'wireless>=0.3.3,<0.4.0']

setup_kwargs = {
    'name': 'progo',
    'version': '0.1.8',
    'description': 'Upside-Down and Backwards™ GoPro - Control your GoPro Hero10.',
    'long_description': "# Progo\n\n\n![Progo](./img/progo.png)\n\n\nAn Upside-Down and Backwards™ implementation of GoPro's Open API.\n\n\n# But first!\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://docs.python.org/3/whatsnew/3.9.html)\n\n\n# Frequently Asked Questions\n\n- WTF would you do this?\n    - I bought a Hero10 and wanted to see how it works. And what can be done with it.\n    - I also wanted an excuse to use [attrs](https://www.attrs.org/en/stable/index.html).\n\n- What model of GoPro is this compatible with?\n    - Hero10 (Open GoPro API 2.0)\n    - Older models (Open GoPro API 1.0), but with some functionality degradation (shutter/encoding control).\n\n- Does it work with more than one camera?\n    - Good question! If you send me another Hero10 I'll make sure it works 😉.\n\n\n# Installing Progo\n\n    $ pip install progo\n\n\n# Developing Progo\n\n    $ FIXME\n\n",
    'author': 'Jakthom',
    'author_email': 'jake@bostata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jakthom/progo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
