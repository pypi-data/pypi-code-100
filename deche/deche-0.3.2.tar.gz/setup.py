# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deche', 'deche.test_utils']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.3.4,<4.0.0',
 'cloudpickle>=2.0.0,<3.0.0',
 'donfig>=0.6.0,<0.7.0',
 'frozendict>=2.0.6,<3.0.0',
 'fsspec>=2021.10.1,<2022.0.0',
 'pytest-asyncio>=0.16.0,<0.17.0']

extras_require = \
{':extra == "s3"': ['s3fs>=2021.7.0,<2022.0.0']}

setup_kwargs = {
    'name': 'deche',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'Bradley McElroy',
    'author_email': 'bradley.mcelroy@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
