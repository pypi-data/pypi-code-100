# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjk_commons']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML', 'appdirs', 'loguru', 'yodl']

setup_kwargs = {
    'name': 'cjk-commons',
    'version': '3.6.0',
    'description': 'Commons',
    'long_description': None,
    'author': 'Cujoko',
    'author_email': 'cujoko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cujoko/commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
