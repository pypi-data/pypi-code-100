# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_auth', 'fast_auth.auth']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'bcrypt>=3.2.0,<4.0.0',
 'cryptography>=35.0.0,<36.0.0',
 'fastapi>=0.70.0,<0.71.0',
 'passlib>=1.7.4,<2.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'python-jose>=3.3.0,<4.0.0']

entry_points = \
{'console_scripts': ['create_user = fast_auth.auth.auth:create_user_cli',
                     'migrate = fast_auth.migration:create_auth_tables_cli']}

setup_kwargs = {
    'name': 'fast-auth',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Douglas Braga',
    'author_email': 'douglas.braga@modenaesilva.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
