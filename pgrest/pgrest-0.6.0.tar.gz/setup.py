# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgrest']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'pgrest',
    'version': '0.6.0',
    'description': 'A Python client library for PostgREST APIs. ',
    'long_description': '# pgrest-client\n\nPostgREST client for Python. This library provides an ORM interface to PostgREST.\n\nFork of the supabase community Postgrest Client library for Python.\n\n[Documentation](https://anand2312.github.io/pgrest)\n\n## TODOS:\n\n- upsert methods\n- AND/OR filtering\n- allow users to pass response models?\n',
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
