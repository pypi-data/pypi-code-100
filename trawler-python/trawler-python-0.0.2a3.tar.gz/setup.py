# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['trawler', 'trawler.agent', 'trawler.sql']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'pandas>=1.3.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'schedule>=1.1.0,<2.0.0']

extras_require = \
{'sql': ['SQLAlchemy>=1.4.17,<2.0.0', 'psycopg2-binary>=2.9.1,<3.0.0']}

entry_points = \
{'console_scripts': ['trawler = trawler.agent.main:main']}

setup_kwargs = {
    'name': 'trawler-python',
    'version': '0.0.2a3',
    'description': 'Trawler is an open source metadata platform for mapping and monitoring your data',
    'long_description': '# trawler python tools\nThese are the Python APIs for trawler',
    'author': 'Alex Sparrow',
    'author_email': 'alex@alexsparrow.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
