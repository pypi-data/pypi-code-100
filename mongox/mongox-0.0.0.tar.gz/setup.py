# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mongox',
    'version': '0.0.0',
    'description': 'Python Mongodb ODM using Pydantic',
    'long_description': '',
    'author': 'Amin Alaee',
    'author_email': 'mohammadamin.alaee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aminalaee/mongox',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
