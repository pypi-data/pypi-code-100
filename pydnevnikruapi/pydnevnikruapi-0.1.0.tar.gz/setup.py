# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydnevnikruapi', 'pydnevnikruapi.aiodnevnik', 'pydnevnikruapi.dnevnik']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'pydnevnikruapi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kesha1225',
    'author_email': 'samedov03@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
