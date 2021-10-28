# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keep_exporter']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click-config-file>=0.6.0,<0.7.0',
 'click>=8.0.1,<9.0.0',
 'gkeepapi>=0.13.4,<0.14.0',
 'mdutils>=1.3.0,<2.0.0',
 'pathvalidate>=2.3.2,<3.0.0',
 'python-frontmatter>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['keep_export = keep_exporter.cli:main']}

setup_kwargs = {
    'name': 'keep-exporter',
    'version': '2.0.1',
    'description': 'Google Keep note exporter utility',
    'long_description': '# Keep-Exporter\n[\n![PyPi](https://img.shields.io/pypi/v/keep-exporter)\n![PyPi](https://img.shields.io/pypi/pyversions/keep-exporter)\n![PyPi](https://img.shields.io/pypi/l/keep-exporter)\n](https://pypi.org/project/keep-exporter/)\n\nA command line utility to export Google Keep notes to markdown files with metadata stored as a frontmatter header. \n\n## Features\n\n * Exports all note types (List and Note)\n * Exports all media attached to notes\n   * Audio, drawings, attached images, etc\n * Sync Keep to directory (keeps directory looking exactly the same as Google Keep)\n * Customizable date format\n   * Easy ISO8601 via `--iso8601`\n * Password or token based authentication\n   * Store your login token to config file with `keep_export savetoken`\n * Note metadata header in yaml frontmatter format\n\n\n## Usage\nIf you do not supply a username or password before running it, you will be prompted to input them.\n```\nUsage: keep_export [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --config FILE                   Read configuration from FILE.  [default: /home/nate/.config/keep-exporter]\n  -u, --user TEXT                 Google account email (prompt if empty)  [env var: GKEEP_USER;required]\n  -p, --password TEXT             Google account password (prompt if empty). Either this or token is required.  [env var: GKEEP_PASSWORD]\n  -t, --token TEXT                Google account token from prior run. Either this or password is required.\n  -d, --directory DIRECTORY       Output directory for exported notes  [default: ./gkeep-export]\n  --header / --no-header          Choose to include or exclude the frontmatter header  [default: header]\n  --delete-local / --no-delete-local\n                                  Choose to delete or leave as-is any notes that exist locally but not in Google Keep  [default: no-delete-local]\n  --rename-local / --no-rename-local\n                                  Choose to rename or leave as-is any notes that change titles in Google Keep  [default: no-rename-local]\n  --date-format TEXT              Date format to prefix the note filenames. Reflects the created date of the note. uses strftime()  [default: %Y-%m-%d]\n  --iso8601                       Format dates in ISO8601 format.\n  --skip-existing-media / --no-skip-existing-media\n                                  Skip existing media if it appears unchanged from the local copy.  [default: skip-existing-media]\n  -h, --help                      Show this message and exit.\n\nCommands:\n  savetoken  Saves the master token to your configuration file.\n```\n\n### Notes\nIf you are using 2 Factor Authentication (2FA) for your google account, you will need to generate an app password for keep. You can do so on your [Google account management page.](https://myaccount.google.com/apppasswords)\n\n\n## Installation\nThere are many ways to install this, easiest is through pip or the releases page.\n\n### Pip\nThe easiest way is with [pip from PyPi](https://pypi.org/project/keep-exporter/)\n```\npip3 install keep-exporter\n```\n\n### Download the Wheel\nDownload the wheel from the [releases page](https://github.com/ndbeals/keep-exporter/releases) and then install with pip:\n```\npip install keep_exporter*.whl\n```\n\n### Building\n#### Download or git clone\n 1. Clone the repository `https://github.com/ndbeals/keep-exporter` or download from the [releases page](https://github.com/ndbeals/keep-exporter/releases) and extract the source code.\n 2. `cd` into the extracted directory\n 3. With [poetry](https://python-poetry.org/) installed, run `poetry install` in the project root directory\n 4. `poetry build` will build the installable wheel\n 5. `cd dist` then run `pip3 install <keep-exporter-file.whl>`\n\n\n## Troubleshooting\nSome users have had issues with the requests library detailed in [this issue](https://github.com/ndbeals/keep-exporter/issues/1) when using `pipx`. The solution is to change the requests library version.\n```\npipx install keep-exporter \npipx inject keep-exporter requests===2.23.0\n```\n',
    'author': 'Nathan Beals',
    'author_email': 'ndbeals@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ndbeals/keep-exporter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
