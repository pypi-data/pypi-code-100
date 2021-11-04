# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ou_container_content',
 'ou_container_content.frontend',
 'ou_container_content.frontend.build']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.3,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'tornado>=6.1,<7.0']

entry_points = \
{'console_scripts': ['ou-container-content = '
                     'ou_container_content.__main__:main']}

setup_kwargs = {
    'name': 'ou-container-content',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mark Hall',
    'author_email': 'mark.hall@open.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
