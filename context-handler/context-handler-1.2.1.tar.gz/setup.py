# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['context_handler', 'context_handler.adapters']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.10.0,<4.0.0']

extras_require = \
{'fastapi': ['fastapi>=0.70.0,<0.71.0'], 'sanic': ['sanic>=21.9.1,<22.0.0']}

setup_kwargs = {
    'name': 'context-handler',
    'version': '1.2.1',
    'description': '',
    'long_description': None,
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
