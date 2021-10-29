# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['huum']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

extras_require = \
{'aiohttp': ['aiohttp>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'huum',
    'version': '0.2.0',
    'description': 'Python library for Huum saunas',
    'long_description': None,
    'author': 'Frank Wickström',
    'author_email': 'frwickst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
