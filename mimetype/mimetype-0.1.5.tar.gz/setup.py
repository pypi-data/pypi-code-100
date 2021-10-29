# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mimetype']

package_data = \
{'': ['*']}

install_requires = \
['enumb>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'mimetype',
    'version': '0.1.5',
    'description': 'Mime Type parsing and creation',
    'long_description': None,
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
