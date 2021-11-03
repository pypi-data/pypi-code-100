# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raspberry_epaper']

package_data = \
{'': ['*'], 'raspberry_epaper': ['font/*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'python-box>=5.4.1,<6.0.0',
 'qrcode>=7.3.1,<8.0.0',
 'typer>=0.4.0,<0.5.0',
 'waveshare-epaper>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['epaper = raspberry_epaper.cli:main']}

setup_kwargs = {
    'name': 'raspberry-epaper',
    'version': '0.4.0',
    'description': "A tool to easily use waveshare's e-paper module with Raspberry Pi",
    'long_description': '# Raspberry e-paper utility\n\nA tool to easily use waveshare\'s e-paper module with Raspberry Pi.\n\n## Install\n\n```sh\npip install raspberry-epaper\n```\n\n## Usage\n\n### print\n\nDisplay the image file.\n\n```sh\n# For example, when using 7.5inch e-Paper HAT\n$ epaper print --device="epd7in5" picture.png\n```\n\nRandomly display the image file in a directory.\n\n```sh\n$ epaper print --device="epd7in5" directory\n```\n\nDisplay a text file.\n\n```sh\n$ epaper print --device="epd7in5" sentence.txt\n```\n\nOverlay the QR code on the image.\n\n```sh\n$ epaper print --device="epd7in5" --qr="information about the picture" picture.png\n```\n\n### version\n\nShow version.\n\n```sh\n$ epaper version\n0.1.0\n```\n\n## License\n\nThis software is released under the MIT License, see LICENSE.\nFonts are licensed under the SIL Open Font License, Version 1.1.\n',
    'author': 'yskoht',
    'author_email': 'ysk.oht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yskoht/raspberry-epaper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
