# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobile_env',
 'mobile_env.baselines',
 'mobile_env.core',
 'mobile_env.handlers',
 'mobile_env.scenarios',
 'mobile_env.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.7.0,<2.0.0',
 'gym>=0.17.1,<0.18.0',
 'matplotlib>=3.4,<4.0',
 'numpy>=1.2.0,<2.0.0',
 'pygame>=2.0,<3.0',
 'svgpath2mpl>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'mobile-env',
    'version': '0.2.6',
    'description': 'mobile-env: A minimalist environment for decision making in wireless mobile networks.',
    'long_description': None,
    'author': 'Stefan Schneider',
    'author_email': 'stefan.schneider@upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stefanbschneider/mobile-env',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
