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
    'version': '1.1.0',
    'description': 'Waveshare e-paper package for Python on Raspberry Pi',
    'long_description': "\n# Waveshare e-paper package\n\nWaveshare e-paper package for Python on Raspberry Pi.\nOriginal source is https://github.com/waveshare/e-Paper.\n\n## Install\n\n```sh\npip install waveshare-epaper\n```\n\n## Usage\n\n```python\nimport epaper\n\n# For example, when using 7.5inch e-Paper HAT\nepd = epaper.epaper('epd7in5').EPD()\n\n# init and Clear\nepd.init()\nepd.Clear()\n```\n\n- `epaper.epaper` method takes the model name and returns the e-paper library module.\n- See below for a list of e-paper model names.\n  - https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd\n- For more information on how to use the e-paper library module, please refer to the `e-Paper` part of the wiki below.\n  - [Waveshare Wiki](https://www.waveshare.com/wiki/Main_Page#OLEDs_.2F_LCDs)\n\n## License\n\nThis software is released under the MIT License, see LICENSE.\n",
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
