# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lanote_core']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Migrate>=3.1.0,<4.0.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'python-dotenv>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'lanote-core',
    'version': '0.0.5',
    'description': '',
    'long_description': None,
    'author': 'Viet Ho',
    'author_email': '4677759+VietHo@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
