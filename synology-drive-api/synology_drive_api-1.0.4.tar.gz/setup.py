# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synology_drive_api']

package_data = \
{'': ['*']}

install_requires = \
['optionaldict>=0.1.1,<0.2.0',
 'requests>=2.22.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'simplejson>=3.17.0,<4.0.0']

setup_kwargs = {
    'name': 'synology-drive-api',
    'version': '1.0.4',
    'description': '',
    'long_description': None,
    'author': 'zbjdonald',
    'author_email': 'zbjdonald@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
