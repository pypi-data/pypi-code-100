# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cubes']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['mkdocs-material>=7.3.6,<8.0.0',
          'mkdocs-static-i18n>=0.21,<0.22',
          'lazydocs>=0.4.8,<0.5.0',
          'pydocstyle>=6.1.1,<7.0.0']}

setup_kwargs = {
    'name': 'pycubes',
    'version': '0.2.0',
    'description': 'Library for creating servers and clients Minecraft Java Edition',
    'long_description': "# pyCubes\n\n![PyPI](https://img.shields.io/pypi/v/pyCubes?style=flat) ![example workflow](https://github.com/DavisDmitry/pyCubes/actions/workflows/test.yml/badge.svg) ![example workflow](https://github.com/DavisDmitry/pyCubes/actions/workflows/lint.yml/badge.svg) [![codecov](https://codecov.io/gh/DavisDmitry/pyCubes/branch/master/graph/badge.svg?token=Y18ZNYT4YS)](https://codecov.io/gh/DavisDmitry/pyCubes) ![PyPI - License](https://img.shields.io/pypi/l/pyCubes) [![Downloads](https://pepy.tech/badge/pycubes/month)](https://pepy.tech/project/pycubes) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n---\n[Documentation](https://pycubes.dmitrydavis.xyz/)\n\n---\npyCubes is a library for creating servers and clients Minecraft Java Edition.\n\n**❗ 0.x versions are not stable. The library API is subject to change.**\n\nInstallation:\n\n```bash\npip install pyCubes\n```\n\n## Usage\n\nFirst you need to create application instance:\n\n```python3\nimport cubes\n\napp = cubes.Application()\n```\n\nAfter that add a low-level handler:\n\n```python3\nasync def process_handshake(packet_id: int, packet: cubes.ReadBuffer):\n    print('Protocol version:', packet.varint)\n    print('Server host:', packet.string)\n    print('Server port:', packet.unsigned_short)\n    print('Next state:', cubes.ConnectionStatus(packet.varint))\n\napp.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)\n```\n\nAll that remains is to launch the application:\n\n```python3\napp.run('127.0.0.1', 25565)\n```\n\nA more detailed example can be found [here](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).\n\nAll packages are described [here](https://wiki.vg/Protocol).\n",
    'author': 'Dmitry Davis',
    'author_email': 'dmitrydavis@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DavisDmitry/pyCubes',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
