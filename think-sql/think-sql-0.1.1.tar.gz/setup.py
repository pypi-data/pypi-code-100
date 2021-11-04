# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['think_sql']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0',
 'cacheout>=0.13.1,<0.14.0',
 'dill>=0.3.4,<0.4.0',
 'jsonpath>=0.82,<0.83',
 'loguru>=0.5.3,<0.6.0',
 'pretty-errors>=1.2.24,<2.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'think-sql',
    'version': '0.1.1',
    'description': 'ThinkSQL link think-orm(ThinkPHP)',
    'long_description': None,
    'author': 'hbh112233abc',
    'author_email': 'hbh112233abc@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
