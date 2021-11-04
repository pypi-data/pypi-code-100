# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_bell']

package_data = \
{'': ['*']}

install_requires = \
['12factor-configclasses>=1.0.0,<2.0.0',
 'anyio>=3.3.4,<4.0.0',
 'asyncclick>=8.0.1,<9.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'rich>=10.12.0,<11.0.0',
 'telethon>=1.23,<2.0']

entry_points = \
{'console_scripts': ['tbell = telegram_bell.bell:cli']}

setup_kwargs = {
    'name': 'telegram-bell',
    'version': '0.2.0',
    'description': 'Notify you when something is mentioned in a telegram channel',
    'long_description': None,
    'author': 'Pablo Cabezas',
    'author_email': 'headsrooms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
