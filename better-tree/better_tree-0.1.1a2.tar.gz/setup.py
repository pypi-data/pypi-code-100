# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['better_tree']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.12.0,<11.0.0']

entry_points = \
{'console_scripts': ['better-tree = better_tree.main:run']}

setup_kwargs = {
    'name': 'better-tree',
    'version': '0.1.1a2',
    'description': 'A better tree utility in Python',
    'long_description': "# better-tree\n\n~~Cause regular tree is weak and no alternative (that works) exists.~~\n\nCause I'm bored out of my mind.\n\n## Usage\n\n![Usage](assets/tree_usage.png)\n",
    'author': 'antoniouaa',
    'author_email': 'antoniouaa@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antoniouaa/better-tree',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
