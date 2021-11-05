# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schuylkill', 'schuylkill.tests']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy[speedup]>=0.18.0,<0.19.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'pandas>=1.3.4,<2.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'sparse-dot-topn>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'schuylkill',
    'version': '0.1.1',
    'description': 'Fixing human errors by matching those hard-to-spell words',
    'long_description': None,
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
