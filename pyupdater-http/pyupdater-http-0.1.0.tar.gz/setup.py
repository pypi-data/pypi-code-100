# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyupdater_http']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyupdater-http',
    'version': '0.1.0',
    'description': 'Plugin: HTTP upload support',
    'long_description': None,
    'author': 'Kirill Pinchuk',
    'author_email': 'cybergrind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
