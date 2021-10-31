# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arxiv_post', 'arxiv_post.apps']

package_data = \
{'': ['*']}

install_requires = \
['arxiv>=1.4,<2.0',
 'dateparser>=1.1,<2.0',
 'deepl>=1.2,<2.0',
 'fire>=0.4,<0.5',
 'more-itertools>=8.10,<9.0',
 'playwright>=1.16,<2.0',
 'pylatexenc>=2.10,<3.0',
 'requests>=2.26,<3.0',
 'tomli>=1.2,<2.0']

entry_points = \
{'console_scripts': ['arxiv-post = arxiv_post.cli:main']}

setup_kwargs = {
    'name': 'arxiv-post',
    'version': '0.6.0',
    'description': 'Translate and post arXiv articles to various apps',
    'long_description': '# arxiv-post\n\n[![PyPI](https://img.shields.io/pypi/v/arxiv-post.svg?label=PyPI&style=flat-square)](https://pypi.org/project/arxiv-post/)\n[![Python](https://img.shields.io/pypi/pyversions/arxiv-post.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/arxiv-post/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/arxiv-post/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/arxiv-post/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nTranslate and post arXiv articles to various apps\n\n## Installation\n\n```shell\n$ pip install arxiv-post\n$ playwright install chromium\n```\n\n## Usage\n\nAfter installation, command line interface `arxiv-post` is available, with which you can translate and post arXiv articles to various apps.\nNote that only `slack` app is currently available.\nYou need to [create a custom Slack app to get an URL of incoming webhook](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack).\n\n```shell\n$ arxiv-post slack --keywords deshima \\\n                   --categories astro-ph.IM \\\n                   --target_lang ja \\\n                   --slack_webhook_url <Slack webhook URL>\n```\n\nThe posted article looks like this.\n\n![arxiv-post-slack.png](https://raw.githubusercontent.com/astropenguin/arxiv-post/master/docs/_static/arxiv-post-slack.png)\n\nFor detailed information, see the built-in help by the following command.\n\n```shell\n$ arxiv-post slack --help\n```\n\n## Example\n\nIt may be nice to regularly run the command by some automation tools such as GitHub Actions.\nHere is a live example in which daily (2 days ago) arXiv articles in [astro-ph.GA](https://arxiv.org/list/astro-ph.GA/new) and [astro-ph.IM](https://arxiv.org/list/astro-ph.IM/new) are posted to different channels of a Slack workspace.\n\n- [a-lab-nagoya/astro-ph-slack: Translate and post arXiv articles to Slack](https://github.com/a-lab-nagoya/astro-ph-slack)\n\n## References\n\n- [fkubota/Carrier-Owl: arxiv--> DeepL --> Slack](https://github.com/fkubota/Carrier-Owl): The arxiv-post package is highly inspired by their work.\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/arxiv-post/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
