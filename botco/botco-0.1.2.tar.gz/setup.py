# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botco', 'botco.contrib', 'botco.methods', 'botco.types', 'botco.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'redis>=3.5.3,<4.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'botco',
    'version': '0.1.2',
    'description': '',
    'long_description': '### `botc` - Telegram bot api wrapper\n### Installation\n```\npip install botc\n```\n',
    'author': 'Suhrob',
    'author_email': 'oopanndaa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/malikovss/botc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
