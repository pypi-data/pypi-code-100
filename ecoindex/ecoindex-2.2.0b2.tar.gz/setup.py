# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecoindex']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141,<5.0',
 'sqlmodel>=0.0.4,<0.0.5',
 'undetected-chromedriver>=3.0.3,<4.0.0']

setup_kwargs = {
    'name': 'ecoindex',
    'version': '2.2.0b2',
    'description': 'Ecoindex module provides a simple way to measure the Ecoindex score based on the 3 parameters: The DOM elements of the page, the size of the page and the number of external requests of the page',
    'long_description': '# ECOINDEX PYTHON\n\n![Quality check](https://github.com/cnumr/ecoindex_python/workflows/Quality%20checks/badge.svg)\n[![PyPI version](https://badge.fury.io/py/ecoindex.svg)](https://badge.fury.io/py/ecoindex)\n\nThis basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:\n\n- The number of DOM elements in the page\n- The size of the page\n- The number of external requests of the page\n\n> **Current limitation:** This does not work well with SPA.\n\n## Requirements\n\n- Python ^3.8 with [pip](https://pip.pypa.io/en/stable/installation/)\n- Google Chrome installed on your computer\n\n## Install\n\n```shell\npip install ecoindex\n```\n\n## Use\n\n```python\nimport asyncio\nfrom pprint import pprint\n\nfrom ecoindex import get_ecoindex, get_page_analysis\n\n# Get ecoindex from DOM elements, size of page and requests of the page\necoindex = asyncio.run(get_ecoindex(dom=100, size=100, requests=100))\npprint(ecoindex)\n\n> Ecoindex(grade=\'B\', score=67, ges=1.66, water=2.49)\n\n# Analyse a given webpage with a resolution of 1920x1080 pixel (default)\npage_analysis = asyncio.run(get_page_analysis(url="http://ecoindex.fr"))\npprint(page_analysis)\n\n> Result(width=1920, height=1080, url=HttpUrl(\'http://ecoindex.fr\', scheme=\'http\', host=\'ecoindex.fr\', tld=\'fr\', host_type=\'domain\'), size=422.126, nodes=54, requests=12, grade=\'A\', score=86.0, ges=1.28, water=1.92, date=datetime.datetime(2021, 10, 8, 10, 20, 14, 73831), page_type=None)\n```\n\n## Contribute\n\nYou need [poetry](https://python-poetry.org/) to install and manage dependencies. Once poetry installed, run :\n\n```bash\npoetry install\n```\n\n## Tests\n\n```shell\npoetry run pytest\n```\n\n## [Contributing](CONTRIBUTING.md)\n\n## [Code of conduct](CODE_OF_CONDUCT.md)\n',
    'author': 'Vincent Vatelot',
    'author_email': 'vincent.vatelot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.ecoindex.fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
