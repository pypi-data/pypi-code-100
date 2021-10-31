# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_selfdoc']

package_data = \
{'': ['*'], 'flask_selfdoc': ['templates/*']}

install_requires = \
['Flask>=1.0,<2.0']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctest',
                     'test = run_tests:test']}

setup_kwargs = {
    'name': 'flask-selfdoc',
    'version': '1.2.4a1',
    'description': 'Documentation generator for flask',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
