# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goap', 'goap.algo', 'goap.planner']

package_data = \
{'': ['*']}

extras_require = \
{'plot': ['matplotlib>=3.0', 'networkx>=2.3']}

setup_kwargs = {
    'name': 'goap-ai',
    'version': '2.0.0rc2',
    'description': 'Goal oriented action programming',
    'long_description': None,
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
