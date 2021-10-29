# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansible_cry']

package_data = \
{'': ['*']}

install_requires = \
['ansible', 'plumbum']

entry_points = \
{'console_scripts': ['cry = ansible_cry.cli:CRY.run']}

setup_kwargs = {
    'name': 'ansible-cry',
    'version': '1.0.1',
    'description': 'Encrypt and decrypt ansible-vault string/file: Perfect for external tools.',
    'long_description': '# CRY\nEncrypt and decrypt ansible-vault string/file perfect external tools\n',
    'author': 'Pierre-Yves Langlois',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylanglois/ansible-cry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
