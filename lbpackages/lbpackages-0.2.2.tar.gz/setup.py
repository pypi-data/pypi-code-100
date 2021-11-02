# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lbpackages',
 'lbpackages.createtables',
 'lbpackages.exceptions',
 'lbpackages.models']

package_data = \
{'': ['*'],
 'lbpackages': ['.mypy_cache/*',
                '.mypy_cache/3.7/*',
                '.mypy_cache/3.7/_typeshed/*',
                '.mypy_cache/3.7/collections/*',
                '.mypy_cache/3.7/importlib/*',
                '.mypy_cache/3.7/lbpackages/*',
                '.mypy_cache/3.7/lbpackages/createtables/*',
                '.mypy_cache/3.7/lbpackages/exceptions/*',
                '.mypy_cache/3.7/lbpackages/models/*',
                '.mypy_cache/3.7/os/*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0']

setup_kwargs = {
    'name': 'lbpackages',
    'version': '0.2.2',
    'description': 'Implements classes for stocks model and db client',
    'long_description': None,
    'author': 'Lionel Barbagallo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
