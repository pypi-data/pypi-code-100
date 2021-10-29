# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cube_practicer']

package_data = \
{'': ['*'], 'cube_practicer': ['resources/*']}

install_requires = \
['pygame>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['cube-practicer = cube_practicer.main:app']}

setup_kwargs = {
    'name': 'cube-practicer',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'ylq',
    'author_email': 'jamesylq@gmail.com',
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
