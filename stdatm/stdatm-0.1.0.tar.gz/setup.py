# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stdatm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17.3,<2.0.0', 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'stdatm',
    'version': '0.1.0',
    'description': 'Numpy-oriented Standard Atmosphere model',
    'long_description': '# StdAtm\nNumpy-oriented Standard Atmosphere model\n',
    'author': 'Christophe DAVID',
    'author_email': 'christophe.david@onera.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
