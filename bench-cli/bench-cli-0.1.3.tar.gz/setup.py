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
    'version': '0.1.3',
    'description': '',
    'long_description': '![bench-logo](https://github.com/mlcgp/bench/blob/master/images/bench-logo.png?raw=true)\n\n<p align="center"><b>Bench is a free, open-source command-line tool and dashboard web app for visualizing stock metrics.</b></p>\n\n<p align="center">\n  <a href="https://github.com/mlcgp/bench/blob/master/LICENSE.txt"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT"></a>\n  <a href="https://pypi.org/project/bench-cli/"><img alt="Pypi Soda SQL" src="https://img.shields.io/badge/pypi-bench--cli-green"></a>\n</p>\n\n![bench-logo](https://github.com/mlcgp/bench/blob/master/images/screengrab.png?raw=true)\n\n[TOC]\n\n## Install Bench\n\nRequirements:\n\n* Python 3.9 or greater\n\nRecommended:\n\n```bash\n$ pip install bench-cli\n```\n\nYou can also install as a dependency within a virtual environment with [poetry](https://python-poetry.org/):\n\n```bash\n$ poetry add bench-cli\n```\n\nOtherwise, clone the project and in the project directory run:\n\n```bash\n$ poetry install\n```\n\n## Use Bench\n\n### Getting Started\n\n#### IEX Cloud\n\nSign up for IEX Cloud and get your API token: https://iexcloud.io/\n\n#### PostgreSQL Database\n\nAll you need to do is create a new Postgres database - that\'s it!\n\nThe SQL queries and API calls are executed with ```$ bench run``` -- that\'s where all the magic happens. The SQL queries can be found [here](https://github.com/mlcgp/bench/tree/master/bench/sql).\n\n### Commands\n\n```bash\n$ bench --install-completion zsh # Installs completion for the shell\n$ bench --show-completion zsh # Shows completion for the shell\n$ bench init # Creates the Bench directory tree at the user\'s home directory\n$ bench init --directory "~/Desktop" # Creates the Bench directory tree at the user\'s home directory and at specified path\n$ bench env # Activates the default .env\n$ bench env --use "~/Desktop/bench/envs/.env" # Activates the .env file at the specified path\n$ bench add "GOOGL" # adds symbol GOOGL to the watchlist\n$ bench remove "FB" # removes symbol FB from the watchlist\n$ bench watchlist # Displays a table of symbols in the watchlist\n$ bench pipeline -i annual -n 10 # Executes the data pipeline for the last 10 years of annual data (-i or --interval can be annual or quarterly)\n$ bench dash # Serves the Dash app at localhost:8050\n```\n\nThe directory structure that ```$ bench init``` creates should look like:\n\n```.\n.\n├── envs\n└── logs\n```\n\n### Environment Configuration\n\nThe .env file should look like this:\n\n```\n# The ENV_PATH is created at ~/bench/envs/.env by default. This variable will also update when a path other than the default is used\nENV_PATH=\'path_to_env\'\n\n# PostgreSQL config\nBENCH_DB_HOST=\'\'\nBENCH_DB_PORT=\'\'\nBENCH_DB_USER=\'\'\nBENCH_DB_NAME=\'\'\nBENCH_DB_PASSWORD=\'\'\n\n# The version can either be \'test\' or \'stable\'. Test will use the IEX Cloud Sandbox API and the test token\nBENCH_IEX_VERSION=\'\'\nBENCH_IEX_TOKEN=\'\'\n# IEX Cloud Sandbox API key\nBENCH_IEX_TEST_TOKEN=\'\'\n\n# Can provide a list of symbols in a comma-separated list (eg. \'AAPL,GOOGL,MSFT\'), or use the add and remove commands\nBENCH_WATCHLIST=\'\'\n```\n\n## Roadmap\n\n| Feature                                            | Completed | Priority |\n| :------------------------------------------------- | --------- | -------- |\n| Add option to ```$ bench dash``` to specify a port | N         | ***      |\n| Data dictionary of supported metrics               | N         | ***      |\n| Detailed logger and reports                        | N         | ***      |\n| Tests                                              | N         | ***      |\n| Add pipelines for other data sources               | N         | *        |\n| Job scheduler for the pipeline                     | N         | *        |\n| DMD for the database                               | N         | *        |',
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
