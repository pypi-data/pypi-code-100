# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyupdater_http']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0']

entry_points = \
{'pyupdater.plugins': ['http_uploader = pyupdater_http.uploader:HTTPUploader']}

setup_kwargs = {
    'name': 'pyupdater-http',
    'version': '0.4.0',
    'description': 'Plugin: HTTP upload support',
    'long_description': None,
    'author': 'Kirill Pinchuk',
    'author_email': 'cybergrind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
