# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diss', 'diss.domains']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.0,<22.0',
 'funcy>=1.16,<2.0',
 'numpy>=1.21.2,<2.0.0',
 'python-sat>=0.1.7.dev11,<0.2.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'diss',
    'version': '0.1.1',
    'description': 'Demonstration Informed Specification Search',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
