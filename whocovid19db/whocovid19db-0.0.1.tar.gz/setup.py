# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whocovid19db']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0', 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'whocovid19db',
    'version': '0.0.1',
    'description': '',
    'long_description': '# WHO Covid-19 Database\nExport the [WHO Covid-19 Database](https://search.bvsalud.org/global-literature-on-novel-coronavirus-2019-ncov/) to a Pandas DataFrame.\n\n## Installation\n```$ pip install whocovid19db```\n\n## Usage\n```# Import the Exporter class:\nfrom whocovid19db import Exporter\n\n# Create a new instance:\nexp = Exporter()\n\n# Export 5 documents from 2021/Oct/29 to 2021/Oct/30:\ndf = exp.get_df(date_interval=(20211029, 20211030), count=5)\n```',
    'author': 'Lucas Lopes',
    'author_email': 'lucaslopesf2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
