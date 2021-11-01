# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bench']

package_data = \
{'': ['*'], 'bench': ['assets/*', 'sql/*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0',
 'alive-progress>=2.1.0,<3.0.0',
 'dash-bootstrap-components>=1.0.0,<2.0.0',
 'dash>=2.0.0,<3.0.0',
 'inflection>=0.5.1,<0.6.0',
 'pandas>=1.3.3,<2.0.0',
 'plotly-express>=0.4.1,<0.5.0',
 'psycopg2>=2.9.1,<3.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'python-dotenv>=0.19.1,<0.20.0',
 'requests-futures>=1.0.0,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'schedule>=1.1.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['bench = cli:app']}

setup_kwargs = {
    'name': 'bench-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '<p align="center"><img src="https://github.com/mlcgp/bench/blob/master/images/bench-logo.png" alt="Bench logo" width="300" /></p>\n\n## Install Bench\n\n```bash\npip install bench\n```\n\n',
    'author': 'Malcolm Gillespie',
    'author_email': 'malcolmgillespie@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mlcgp/bench-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
