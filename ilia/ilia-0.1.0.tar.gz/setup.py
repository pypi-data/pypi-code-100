# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ilia', 'ilia.dialects']

package_data = \
{'': ['*']}

install_requires = \
['httpx[brotli,http2]>=0.20.0,<0.21.0',
 'pytest-subtests>=0.5.0,<0.6.0',
 'types-dataclasses>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'ilia',
    'version': '0.1.0',
    'description': 'a JSON Schema draft 2020-12 validation library',
    'long_description': '# ilia\n',
    'author': 'Xavier Barbosa',
    'author_email': 'clint.northwood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lab.errorist.xyz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
