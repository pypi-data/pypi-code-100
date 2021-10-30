# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tedpy']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'tedpy',
    'version': '0.2.0',
    'description': 'Unofficial library for reading from The Energy Detective power meters',
    'long_description': "# TEDpy\n\nUnofficial library for reading from The Energy Detective power meters\n\nThis library supports the TED5000 and TED6000 devices.\n\nIt is based on @realumhelp's [ted6000py](https://github.com/realumhelp/ted6000py), Home Assistant's ted5000 implementation, and @gtdiehl and @jesserizzo's [envoy_reader](https://github.com/gtdiehl/envoy_reader/). Also huge thanks to @realumhelp for patching support for consumption/production distinction!\n\n## Usage\n\n```python\nfrom tedpy import createTED\n\nHOST = 'ted6000'\n\n# Use asyncio to deal with the async methods\nreader = await createTED(HOST)\nawait reader.update()\nreader.print_to_console()\n```\n\n## Testing\n\nTo print out your energy meter's values, run `poetry run python -m tedpy`.\n\nThe module's tests can be run using `poetry run pytest` (make sure you `poetry install` first!).\n\n## Development\n\n1. Install dependencies: `poetry install`\n2. Install pre-commit hooks: `poetry run pre-commit install`\n3. Develop!\n",
    'author': 'rianadon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rianadon/the-energy-detective-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
