# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phl_courts_scraper',
 'phl_courts_scraper.court_summary',
 'phl_courts_scraper.docket_sheet',
 'phl_courts_scraper.portal']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'intervaltree>=3.1.0,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.3.3,<2.0.0',
 'pdfplumber>=0.5.28,<0.6.0',
 'selenium>=4.0.0,<5.0.0',
 'tryagain>=1.0,<2.0',
 'webdriver-manager>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'phl-courts-scraper',
    'version': '0.1.1',
    'description': 'A Python utility to scrape docket sheets and court summaries for Philadelphia courts.',
    'long_description': None,
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
