# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.extractorutils.cogex']

package_data = \
{'': ['*']}

install_requires = \
['cognite-extractor-utils>=1.5.3,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['cogex = cognite.extractorutils.cogex.__main__:main']}

setup_kwargs = {
    'name': 'cognite-extractor-manager',
    'version': '0.1.0',
    'description': 'A project manager for Python based extractors',
    'long_description': None,
    'author': 'Mathias Lohne',
    'author_email': 'mathias.lohne@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
