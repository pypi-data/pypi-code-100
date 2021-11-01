# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vankrupt_workshop_client', 'vankrupt_workshop_client.api']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'dacite>=1.6.0,<2.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['vankrupt_download = '
                     'vankrupt_workshop_client.consumer_cli:cli',
                     'vankrupt_upload = '
                     'vankrupt_workshop_client.creator_cli:cli']}

setup_kwargs = {
    'name': 'vankrupt-workshop-client',
    'version': '0.3.0',
    'description': 'Reference clients for vankrupt workshop',
    'long_description': "# Vankrupt workshop clients\nHere you'll find reference implementations of clients \nfor interacting with vankrupt workshop APIs.\n\nThe library comes with a relatively thin API and CLI clients for \nboth uploading mods, and downloading/upgrading them. \n\n## API library\nAPI client/library [readme](vankrupt_workshop_client/api/README.md) \nwill be most helpful for you, if you are looking for references \non how to implement uploader/downloader clients.\nThe documentation on how exactly to process downloads, updates, \nperform uploads is there as well.\n\n## CLI client\nCLI client [readme](vankrupt_workshop_client/README.md) \nis a good reference on how exactly to use API clients and tie them up\nto a concrete environment.\n\n\n## General info / status\nIt works against the environment you choose, both cli clients can be configured\nto work with `dev / prod / local` environments.\n\nCurrently it works against dev by default. When prod gets pulished, will \nwork with that.\n\n\n## Installation\nThe library is published to PyPi under the name \n[vankrupt-workshop-client](https://pypi.org/project/vankrupt-workshop-client).\n\nThus, to use it locally all you'd need to do is install it.\nI'd recommend to do it the following way:\n1. Create python virtual env:\n    ```shell script\n    python3 -m venv venv\n    ```\n2. Activate it:\n    ```shell script\n    source venv/bin/activate\n    ```\n3. Install:\n    ```shell script\n    pip install vankrupt-workshop-client\n    ```\n4. Use however you'd like, i.e.:\n    ```shell script\n    vankrupt_download filter-mods --page 1 --platform ps5\n    ```\n   For usage details, refer to \n   CLI client [readme](vankrupt_workshop_client/README.md).\n\nQuickstart: run\n\n1. Download\n    ```shell script\n    vankrupt_download --help\n    ```\n\n2. Upload\n    ```shell script\n    vankrupt_upload --help\n    ```\n",
    'author': 'MeRuslan',
    'author_email': 'clanghopper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
