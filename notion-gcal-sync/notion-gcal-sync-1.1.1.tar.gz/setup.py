# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_gcal_sync', 'notion_gcal_sync.clients', 'notion_gcal_sync.events']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'google-api-python-client==2.23.0',
 'google-auth-oauthlib==0.4.6',
 'notion-client==0.7.0',
 'pandas==1.3.3',
 'pyyaml==5.4.1']

entry_points = \
{'console_scripts': ['notion-gcal-sync = notion_gcal_sync.__main__:main']}

setup_kwargs = {
    'name': 'notion-gcal-sync',
    'version': '1.1.1',
    'description': 'Bidirectional synchronize calendar events within notion and google calendar',
    'long_description': '[![CI](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Ravio1i/notion-gcal-sync/actions/workflows/ci.yml)\n[![PyPI version](https://badge.fury.io/py/notion-gcal-sync.svg)](https://badge.fury.io/py/notion-gcal-sync)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# Notion-GCal-Sync\n\nNotion-GCal-Sync is a python application to bidirectional synchronize calendar events within notion and google calendar.\n\n## Getting started\n\n1. Install package from [PyPi](https://pypi.org/project/notion-gcal-sync/)\n\n    ```bash\n    pip install notion-gcal-sync\n    ```\n\n2. Get your Google Calendar `credentials.json` [like this](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-credentials-for-google-calendar)\n3. Get your Notion Token [like this](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-credentials-for-notion)\n4. Set up the Notion page [like this]((https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md#setup-up-your-notion-page))\n5. Create config folder `~/.notion-gcal-sync` and copy the `credentials.json` inside\n\n    **Linux (or WSL)**\n    ```bash\n    cp ~/Downloads/client_secret_*.apps.googleusercontent.com.json "~/.notion-gcal-sync/client_secret.json"\n    ```\n\n    **Windows**\n    Copy your `client_secret_*.apps.googleusercontent.com.json` as `client_secret.json` inside `C:\\Users\\dude\\.notion-gcal-sync`\n    ```powershell\n    # TODO\n    ```\n\n\n6. Run the script and fill out the prompts. If not sure skip the optional bits.\n   1. Make [sure you get your timezone right](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)\n      1. Use your TZ database name as `timezone_name`\n      2. Use the UTC DST offset as `timezone_diff`\n   2. `google_mail`: Your mail you are using in google calendar want to have synced\n   3. `notion_database_url` The url for the page you set up in 4.\n   4. `notion_token`: The token you set up in 3.\n\n    ```bash\n    notion-gcal-sync\n\n    2021-10-28 19:55:41,198 [INFO] /home/worker/.notion-gcal-sync/config.yml does not exist\n    Create non-existing /home/worker/.notion-gcal-sync/config.yml? [Y/n]: y\n    2021-10-28 19:55:42,630 [INFO] Configuring /home/worker/.notion-gcal-sync/config.yml\n    default_event_length [60]:\n    no_date_action [skip]:\n    timezone_name [Europe/Berlin]:\n    timezone_diff [+02:00]:\n    google_mail (e.g name@gmail.com): cooldude@gmail.com\n    notion_database_url [https://www.notion.so/***?v=***&p=]:\n    notion_token: secret_ASDFASDFCASDF\n    ```\n\n7. It will prompt you to authenticate yourself for google. This will create a `token.json`.\n\n    ```bash\n    $ notion-gcal-sync\n    ...\n    Please visit this URL to authorize this application:\n    https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=***\n    ```\n\nFor more information follow [these instructions](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md).\n\n## Usage\n\nMake sure you followed the [setup](https://github.com/Ravio1i/notion-gcal-sync/blob/main/docs/setup.md) and\nconfigured the `config.yml` with your notion token and page for Notion API and gathered and setup\ncredentials `client_secret.json` for Google Calendar API.\n\n```bash\nnotion-gcal-sync\n```\n\n### Docker\nTo run inside the container you need to add the volume at `~/.notion-gcal-sync`\n\n```yaml\ndocker run -v ~/.notion-gcal-sync:/home/worker/.notion-gcal-sync notion-gcal-sync\n```\n\n\nIf you want to update the setup within the cli or only map the credentials, you\'ll need to add interactive mode `-it` and for authenticating a new token you\'ll also need `--net=host`\n\n```yaml\ndocker run --net=host -it \\\n     -v ~/.notion-gcal-sync/client_credentials.json:/home/worker/notion-gcal-sync/client_credentials.json \\\n     notion-gcal-sync\n```\n\nIf you do not want to mount, build it yourself with your credentials.\n\n```Dockerfile\nFROM ghrc.io/ravio1i/notion-gcal-sync\nCOPY token.json /home/worker/token.json\nCOPY config.yml /home/worker/config.json\n```\n\n## Notes\n\nBE AWARE OF THE FOLLOWING:\n\n* This sync will update your source links in gcal. Links to mail etc. will get overwritten with a link to the notion page. The\n  original links will be put on top of the description\n* This sync will update all your invites from other calendars not specified to your default calendar. There is a button on gcal\n  to restore back\n* Goals defined from calendar apps are skipped.\n* Recurrent original events are skipped. Recurrent occurrences of events are created one by one in notion. Changing in notion\n  will change only an occurrence in GCal.\n\nWith around ~2500 events in gcal the sync:\n\n* to get all events took ~1min\n',
    'author': 'Luka Kroeger',
    'author_email': 'luka.kroeger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ravio1i/notion-gcal-sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
