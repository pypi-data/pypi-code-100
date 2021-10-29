# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stackmorelayers']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.0,<2.0',
 'lightgbm>=3.2.1,<4.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21,<2.0',
 'pandas>=1.3.3,<2.0.0',
 'scikit-learn>=1.0,<2.0',
 'statsmodels>=0.12.2,<0.13.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'stackmorelayers',
    'version': '0.0.6',
    'description': 'My personal ML library',
    'long_description': None,
    'author': 'Andrew Sonin',
    'author_email': 'sonin.cel@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewsonin/stackmorelayers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
