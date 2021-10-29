# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pixii']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.19.6,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pixii',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Kevin Duff',
    'author_email': 'kevinkelduff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/k2bd/pixii',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
