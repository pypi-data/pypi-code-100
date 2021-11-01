# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bump_semver_anywhere']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pytomlpp>=1.0.3,<2.0.0', 'semver>=2.13.0,<3.0.0']

entry_points = \
{'console_scripts': ['bump_semver_anywhere = bump_semver_anywhere.cli:main',
                     'bump_semver_anywhere = bump_semver_anywhere.cli:main']}

setup_kwargs = {
    'name': 'bump-semver-anywhere',
    'version': '0.1.1',
    'description': 'Bump your semantic version of any software using regex',
    'long_description': None,
    'author': 'Ivan Gonzalez',
    'author_email': 'scratchmex@gmail.com',
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
