# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postgres_fixture']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0', 'click>=8.0.3,<9.0.0', 'psycopg2>=2.9.1,<3.0.0']

entry_points = \
{'console_scripts': ['pg_fx = '
                     'postgres_fixture.postgres_fixture:postgres_fixture']}

setup_kwargs = {
    'name': 'postgres-fixture',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
