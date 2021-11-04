# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psql2bigquery', 'psql2bigquery.tools']

package_data = \
{'': ['*']}

install_requires = \
['click', 'google-cloud-bigquery', 'psycopg2-binary']

extras_require = \
{'sentry': ['sentry-sdk']}

entry_points = \
{'console_scripts': ['psql2bigquery = psql2bigquery.main:cli']}

setup_kwargs = {
    'name': 'psql2bigquery',
    'version': '0.0.3',
    'description': 'Export PostgreSQL databases to Google Cloud Platform BigQuery',
    'long_description': "# PostgreSQL to BigQuery\n\nInstall with: `pip install psql2bigquery`\n\nGet usage instructions with: `psql2bigquery run --help`\n\n## Sample usage\n\n```\npoetry run psql2bigquery run \\\n--db-host localhost \\\n--db-port 5432 \\\n--db-user username \\\n--db-password secret-password \\\n--db-name my_api \\\n--gcp-project my-project \\\n--gcp-dataset my_api \\\n--include table_name_a \\\n--include table_name_b \\\n--gcp-credential-path /path/to/credential.json\n```\n\n## Logging\n\nThere's a possibility to use Sentry.io for error logging.\n\nJust set the environment variable `SENTRY_DSN` and psql2bigquery will automatically configure the logger.\n\nAdditionally, the environment variable `ENV` can be used as Sentry environment.\n\n\n## Contributing\n\n- Fork this project\n- Install dependencies with `make dependencies`\n  - Make sure you have Python 3 installed. (pyenv)[https://github.com/pyenv/pyenv#installation] is highly recommended\n- You can test the client locally (without installing the package) with `poetry run psql2bigquery <command>`\n- Make a PR with as much details as possible\n",
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CraveFood/psql2bigquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
