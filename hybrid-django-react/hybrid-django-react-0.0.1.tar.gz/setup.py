# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hybrid_django_react']

package_data = \
{'': ['*'],
 'hybrid_django_react': ['assets/*',
                         'assets/.vscode/*',
                         'assets/frontend/*',
                         'assets/locale/*',
                         'assets/static/*',
                         'assets/templates/*']}

setup_kwargs = {
    'name': 'hybrid-django-react',
    'version': '0.0.1',
    'description': 'Django starter project template. Dockerized Django serving a static React app',
    'long_description': None,
    'author': 'gmso',
    'author_email': 'german.mene@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
