# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epaper',
 'epaper.e-Paper.RaspberryPi_JetsonNano',
 'epaper.e-Paper.RaspberryPi_JetsonNano.python',
 'epaper.e-Paper.RaspberryPi_JetsonNano.python.lib',
 'epaper.e-Paper.RaspberryPi_JetsonNano.python.lib.waveshare_epd']

package_data = \
{'': ['*']}

install_requires = \
['RPi.GPIO>=0.7.0,<0.8.0', 'spidev>=3.5,<4.0']

setup_kwargs = {
    'name': 'waveshare-epaper',
    'version': '1.1.1',
    'description': 'Waveshare e-paper package for Python on Raspberry Pi',
    'long_description': '\n# Waveshare e-paper package\n\nWaveshare e-paper package for Python on Raspberry Pi.\nOriginal source is https://github.com/waveshare/e-Paper.\n\n## Install\n\n```sh\npip install waveshare-epaper\n```\n\n## Usage\n\nYou can get available e-paper modules list by `epaper.modules()`.\n\n```python\n$ python\nPython 3.7.3 (default, Jan 22 2021, 20:04:44)\n[GCC 8.3.0] on linux\nType "help", "copyright", "credits" or "license" for more information.\n>>> import epaper\n>>> epaper.modules()\n[\'epd1in02\', \'epd1in54\', \'epd1in54_V2\', \'epd1in54b\', \'epd1in54b_V2\', \'epd1in54c\', \'epd2in13\', \'epd2in13_V2\', \'epd2in13b_V3\', \'epd2in13bc\', \'epd2in13d\', \'epd2in66\', \'epd2in66b\', \'epd2in7\', \'epd2in7b\', \'epd2in7b_V2\', \'epd2in9\', \'epd2in9_V2\', \'epd2in9b_V3\', \'epd2in9bc\', \'epd2in9d\', \'epd3in7\', \'epd4in01f\', \'epd4in2\', \'epd4in2b_V2\', \'epd4in2bc\', \'epd5in65f\', \'epd5in83\', \'epd5in83_V2\', \'epd5in83b_V2\', \'epd5in83bc\', \'epd7in5\', \'epd7in5_HD\', \'epd7in5_V2\', \'epd7in5b_HD\', \'epd7in5b_V2\', \'epd7in5bc\']\n```\n\n- See below for a list of e-paper model names.\n  - https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd\n- For more information on how to use the e-paper library module, please refer to the `e-Paper` part of the wiki below.\n  - [Waveshare Wiki](https://www.waveshare.com/wiki/Main_Page#OLEDs_.2F_LCDs)\n\n<br />\n\n`epaper.epaper` method takes the model name and returns the e-paper library module.\n\n```python\nimport epaper\n\n# For example, when using 7.5inch e-Paper HAT\nepd = epaper.epaper(\'epd7in5\').EPD()\n\n# init and Clear\nepd.init()\nepd.Clear()\n```\n\n## License\n\nThis software is released under the MIT License, see LICENSE.\n',
    'author': 'yskoht',
    'author_email': 'ysk.oht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yskoht/waveshare-epaper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
