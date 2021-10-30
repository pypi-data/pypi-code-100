# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotgbotapi']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.0,<0.71.0',
 'httptools>=0.3.0,<0.4.0',
 'httpx[http2]>=0.20.0,<0.21.0',
 'pydantic>=1.8.2,<2.0.0',
 'ujson>=4.2.0,<5.0.0',
 'uvicorn>=0.15.0,<0.16.0',
 'uvloop>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['tgen = generator.main:main']}

setup_kwargs = {
    'name': 'aiotgbotapi',
    'version': '0.1.0',
    'description': 'Asynchronous Telegram BOT API Client',
    'long_description': '# aiotgbotapi - Asynchronous Telegram BOT API Client',
    'author': 'Pylakey',
    'author_email': 'pylakey@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylakey/aiotgbotapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
