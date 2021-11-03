# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mikroj',
 'mikroj.actors',
 'mikroj.parsers',
 'mikroj.parsers.code',
 'mikroj.parsers.definition',
 'mikroj.registries',
 'mikroj.ui']

package_data = \
{'': ['*'], 'mikroj': ['assets/*', 'plugins/*']}

install_requires = \
['Markdown>=3.3.4,<4.0.0',
 'PyQt5>=5.15.4,<6.0.0',
 'arkitekt>=0.1.89,<0.2.0',
 'mikro>=0.1.40,<0.2.0',
 'pyimagej>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['mikroj = mikroj.run:main']}

setup_kwargs = {
    'name': 'mikroj',
    'version': '0.1.16',
    'description': '',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
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
