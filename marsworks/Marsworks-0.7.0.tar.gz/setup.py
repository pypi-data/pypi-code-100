# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marsworks', 'marsworks.origin']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'marsworks',
    'version': '0.7.0',
    'description': "An API Wrapper around NASA's Mars Rover Photos API written in Python; providing sync and async support.",
    'long_description': '<img src=https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia23378-16.jpg class="center">\n\n<p align="center">\n <img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white">\n\n <img alt="PyPI version" src="https://badge.fury.io/py/marsworks.svg" height=28>\n\n\n<img src="https://img.shields.io/pypi/l/marsworks" height=28>\n\n <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" height=28>\n</p>\n\n\n# Welcome!\n\nHi! Welcome to my repository Marsworks! (Name\ninspired from fate franchise ofc ;) ).\n\nSo, Marsworks is a fast and lightweight API wrapper around\n[Mars Rover Photos API](https://api.nasa.gov/) written in Python.\n\nLet\'s see why you should or shouldn\'t use this wrapper in next sections.\n\n### Advantages\n\n- Sync & Async support with Async utilizing async-await syntax.\n- Fast, lightweight; and memory optimized.\n- Provides API request handling at really low as\nwell as high level.\n- 100% API coverage.\n- Pagination supported.\n- Minimal dependency of just 1 for both sync & async support.\n\n### Disadvantages\n\n- No Caching.\n- No Ratelimit handling or request quering.\n- Not well tested.\n\n*Currently this project is under development and possibilities of\nbreaking changes in near future is huge until 1.x release.*\n\n## Usage\n\n#### Async. usage\n\n###### Getting photos on a particular sol taken by this rover, asynchronously.\n\n```py\n\nimport asyncio\n\nimport marsworks\n\n\nclient = marsworks.AsyncClient()\n\n\nasync def main(rover_name, sol) -> list:\n    images = await client.get_photo_by_sol(rover_name, sol)  # You can pass camera too.\n    return images\n\n\nimgs = asyncio.run(main("Curiosity", 956))\nprint(imgs[0].img_src)\nprint(imgs[0].photo_id)\n# and many more attributes!\n```\n\n#### Sync. usage\n\n###### Getting photos on a particular sol taken by this rover, synchronously.\n\n```py\n\nimport marsworks\n\n\nclient = marsworks.SyncClient()\n\n\ndef main(rover_name, sol) -> list:\n    images = client.get_photo_by_sol(rover_name, sol)  # You can pass camera too.\n    return images\n\n\nimgs = main("Curiosity", 956)\nprint(imgs[0].img_src)\nprint(imgs[0].photo_id)\n# and many more attributes!\n```\n\n\n# Links\n\n- #### Marsworks [Documentation](https://mooncell07.github.io/Marsworks/).\n\n- #### Marsworks PyPi [Page](https://pypi.org/project/marsworks/).\n\n- #### NASA APIs [Page](https://api.nasa.gov/).\n\n- #### Thanks to [Andy](https://github.com/an-dyy) for his contribution.\n',
    'author': 'mooncell07',
    'author_email': 'mooncell07@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mooncell07/Marsworks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
