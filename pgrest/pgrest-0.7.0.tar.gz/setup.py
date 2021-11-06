# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgrest']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0', 'multidict>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'pgrest',
    'version': '0.7.0',
    'description': 'A Python client library for PostgREST APIs. ',
    'long_description': '# pgrest\n\nPostgREST client for Python. This library provides an ORM interface to PostgREST.\n\nFork of the supabase community Postgrest Client library for Python.\n\n[Documentation](https://anand2312.github.io/pgrest)\n\n## TODOS:\n\n[] upsert methods\n[x] AND/OR filtering (v0.6.0)\n[] allow users to pass response models?\n[] add configuration parameter to text-search functions\n',
    'author': 'Anand Krishna',
    'author_email': 'anandkrishna2312@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anand2312/pgrest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
