# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jm_dep1']

package_data = \
{'': ['*']}

install_requires = \
['protobuf==3.17.2']

setup_kwargs = {
    'name': 'jm-dep1',
    'version': '0.3',
    'description': '',
    'long_description': None,
    'author': 'Jean-Mark Wright',
    'author_email': 'jeanmark.wright@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
