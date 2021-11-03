# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kontrctl', 'kontrctl.commands', 'kontrctl.utils']

package_data = \
{'': ['*']}

install_requires = \
['click', 'coloredlogs', 'kontr-api', 'pyyaml', 'tabulate']

entry_points = \
{'console_scripts': ['kontrctl = kontrctl.cli:cli_main']}

setup_kwargs = {
    'name': 'kontrctl',
    'version': '0.6.0',
    'description': 'Kontr portal CLI',
    'long_description': '# Kontrctl - Kontr portal CLI client\n\n`kontrctl` - Kontr Portal management CLI Tool\n\n\n## Setup\n\nThere are multiple variants how to install and run the `kontrctl`.\n\n\n### Install from pypi registry\n\nThe best way to install the `kontrctl` is using the `pip`.\n\n```bash\npip install kontrctl\n```\n\n### Install from source\n\nFor development purposes clone the repository and install dependencies using the pipenv\n\n```bash\ngit clone https://gitlab.fi.muni.cz/grp-kontr2/kontrctl\npipenv install\n```\n\nUpdate `kontr-api` (optional)\n\n```bash\npipenv update kontr-api\npipenv shell\n```\n\n## Run the `kontrctl`\n\n```\nkontrctl --help\n```\n\n## Development run\n\nRun the development version\n\n```bash\npython -m kontrctl.cli --help\n```\n\n## First run setup\n\nBefore using the `kontrctl` to manage the portal and submit, you need to set remote\n\n```bash\nkontrctl remotes add default https://kontr.fi.muni.cz\nkontrctl remotes select default\nkontrctl login  # Provide username and password\n```\n\n### Remotes\n\nRemote sets location and default params for the kontr instance\n\n```bash\nkontrctl remotes --help\nkontrctl remotes list\nkontrctl remotes add <name> <url>\nkontrctl remotes rm <name>\nkontrctl remotes read <name>\nkontrctl remotes select <name>\nkontrctl remotes deselect <name> # Not implemented\n```\n\n### Auth\n\nAuthentication commands\n\n#### Login\n\n```bash\nkontrctl login\nkontrctl --help\n```\n\n#### Logout\n\n\n```bash\nkontrctl logout\nkontrctl logout --help\n```\n\n### Users\n\nUsers resources management\n\n```bash\nkontrctl users --help\nkontrctl users list\nkontrctl users read <name>\nkontrctl users delete <name>\n```\n\n### Courses:\nCourses resources management\n\n```bash\nkontrctl courses --help\nkontrctl courses list\nkontrctl courses read <name>\nkontrctl courses delete <name>\nkontrctl courses select <name>\nkontrctl courses deselect\n```\n\n### Components:\nComponents resources management\n\n```bash\nkontrctl components --help\nkontrctl components list\nkontrctl components read <name>\nkontrctl components delete <name>\n```\n\n### Projects:\nProjects resources management\n\n```bash\nkontrctl projects --help\nkontrctl projects list\nkontrctl projects read <name>\nkontrctl projects delete <name>\nkontrctl projects select <name>\nkontrctl projects deselect\n\n# if selected course not provided:\nkontrctl projects list -c <course_name>\n```\n\n### Submit\nCreate new submission\n\n```bash\nkontrctl submit --help\nkontrctl submit -c <course> -p <project> -t git -u <repo_url> -D <subdir>\n\n# Example:\nkontrctl submit -c TestCourse1 -p HW01 -t git -u "https://github.com/pestanko/example-repo" -D <subdir>\n```\n\n## Contributing\n\nTake a look at [General Contribution Guide](https://gitlab.fi.muni.cz/grp-kontr2/kontr-documentation/blob/master/contributing/GeneralContributionGuide.adoc).\n',
    'author': 'Peter Stanko',
    'author_email': 'stanko@mail.muni.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.fi.muni.cz/grp-kontr2/kontrctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
