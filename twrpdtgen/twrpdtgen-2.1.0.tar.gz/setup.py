# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twrpdtgen', 'twrpdtgen.utils']

package_data = \
{'': ['*'], 'twrpdtgen': ['templates/*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0', 'Jinja2>=3.0.0a1,<4.0.0']

setup_kwargs = {
    'name': 'twrpdtgen',
    'version': '2.1.0',
    'description': 'A Python library/script to automatically generate TWRP-compatible device tree from a boot/recovery image',
    'long_description': "# TWRP device tree generator\n\n[![PyPi version](https://img.shields.io/pypi/v/twrpdtgen)](https://pypi.org/project/twrpdtgen/)\n[![PyPi version status](https://img.shields.io/pypi/status/twrpdtgen)](https://pypi.org/project/twrpdtgen/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ded3a853b48b44b298bc3f1c95772bfd)](https://www.codacy.com/gh/SebaUbuntu/TWRP-device-tree-generator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/TWRP-device-tree-generator&amp;utm_campaign=Badge_Grade)\n\nCreate a [TWRP](https://twrp.me/)-compatible device tree only from an Android recovery image (or a boot image if the device uses non-dynamic partitions A/B) of your device's stock ROM\nIt has been confirmed that this script supports images built starting from Android 4.4 up to Android 12\n\n## Installation\n\n```\npip3 install twrpdtgen\n```\nThe module is supported on Python 3.9 and above.\n\nLinux only: Be sure to have cpio installed in your system (Install cpio using `sudo apt install cpio` or `sudo pacman -S cpio` based on what package manager you're using)\n\n## How to use\n\n```\n$ python3 -m twrpdtgen -h\nTWRP device tree generator\nVersion 2.1.0\n\nusage: python3 -m twrpdtgen [-h] [-o OUTPUT] [--git] [-d] image\n\npositional arguments:\n  image                 path to an image (recovery image or boot image if the\n                        device is A/B)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OUTPUT, --output OUTPUT\n                        custom output folder\n  --git                 create a git repo after the generation\n  -d, --debug           enable debugging features\n```\n\nWhen an image is provided, if everything goes well, there will be a device tree at `output/manufacturer/codename`\n\nYou can also use the module in a script, with the following code:\n\n```python\nfrom twrpdtgen.devicetree import DeviceTree\n\n# Get image info\ndevicetree = DeviceTree(image_path)\n\n# Dump device tree to folder\ndevicetree.dump_to_folder(output_path)\n```\n",
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/twrpdtgen/twrpdtgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
