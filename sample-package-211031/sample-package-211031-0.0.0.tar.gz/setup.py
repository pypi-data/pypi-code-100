# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_package_211031', 'sample_package_211031.sample']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0',
 'flake8>=4.0.1,<5.0.0',
 'jupyterlab>=3.2.1,<4.0.0',
 'mypy>=0.910,<0.911',
 'nbstripout>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'sample-package-211031',
    'version': '0.0.0',
    'description': 'sample package',
    'long_description': '# Sample package',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
