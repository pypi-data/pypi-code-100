# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xscaffold']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0', 'PyYAML>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['xscaffold = xscaffold.xscaffold:main']}

setup_kwargs = {
    'name': 'x-scaffold',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Clayton',
    'author_email': 'dclayton@godaddy.com',
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
