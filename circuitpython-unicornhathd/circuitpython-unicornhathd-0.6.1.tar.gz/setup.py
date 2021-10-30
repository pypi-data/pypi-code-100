# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unicornhathd']

package_data = \
{'': ['*']}

install_requires = \
['Adafruit-Blinka>=6.15.0,<7.0.0',
 'adafruit-circuitpython-framebuf>=1.4.7,<2.0.0']

setup_kwargs = {
    'name': 'circuitpython-unicornhathd',
    'version': '0.6.1',
    'description': "CircuitPython framebuf based driver for Pimoroni's Unicorn HAT HD",
    'long_description': "Introduction\n============\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Code Style: Black\n\nCircuitPython framebuf based driver for Pimoroni's Unicorn HAT HD.\nThis driver supports the `adafruit_framebuf interface <https://circuitpython.readthedocs.io/projects/framebuf/en/latest/>`__ via composition instead of inheritance.\n\n.. image:: ./images/unicornhathd_rainbow.png\n   :alt: Pimoroni Unicorn HAT HD on breadboard\n   :scale: 50%\n   :align: center\n\n\nDependencies\n=============\nThis driver depends on:\n\n* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_\n* `Adafruit framebuf <https://github.com/adafruit/Adafruit_CircuitPython_framebuf>`_\n\nPlease ensure all dependencies are available on the CircuitPython filesystem.\nThis is easily achieved by downloading\n`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_\nor individual libraries can be installed using\n`circup <https://github.com/adafruit/circup>`_.\n\nInstalling from PyPI\n=====================\n.. note:: This library is not available on PyPI yet. Install documentation is included\n   as a standard element. Stay tuned for PyPI availability!\n\nOn supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from\nPyPI <https://pypi.org/project/circuitpython-unicornhathd/>`_.\nTo install for current user:\n\n.. code-block:: shell\n\n    pip3 install circuitpython-unicornhathd\n\nTo install system-wide (this may be required in some cases):\n\n.. code-block:: shell\n\n    sudo pip3 install circuitpython-unicornhathd\n\nTo install in a virtual environment in your current project:\n\n.. code-block:: shell\n\n    mkdir project-name && cd project-name\n    python3 -m venv .env\n    source .env/bin/activate\n    pip3 install circuitpython-unicornhathd\n\n\n\nInstalling to a Connected CircuitPython Device with Circup\n==========================================================\n\nMake sure that you have ``circup`` installed in your Python environment.\nInstall it with the following command if necessary:\n\n.. code-block:: shell\n\n    pip3 install circup\n\nWith ``circup`` installed and your CircuitPython device connected use the\nfollowing command to install:\n\n.. code-block:: shell\n\n    circup install unicornhathd\n\nOr the following command to update an existing version:\n\n.. code-block:: shell\n\n    circup update\n\nUsage Example\n=============\n\n.. code-block:: python\n\n  import board\n  import digitalio\n  from unicornhathd import UnicornHATHD\n\n  # TODO: Change this pin to match your wiring\n  chip_select_pin = digitalio.DigitalInOut(board.D0)\n  chip_select_pin.direction = digitalio.Direction.OUTPUT\n  chip_select_pin.value = True\n\n  display = UnicornHATHD(board.SPI(), chip_select_pin)\n\n  # Turn on all of the blue LEDs\n  display.fill(127)\n  display.show()\n\nContributing\n============\n\nContributions are welcome! Please read our `Code of Conduct\n<https://github.com/NathanY3G/CircuitPython_Unicorn_HAT_HD/blob/HEAD/CODE_OF_CONDUCT.md>`_\nbefore contributing to help this project stay welcoming.\n\nDocumentation\n=============\n\nFor information on building library documentation, please check out\n`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.\n",
    'author': 'Nathan Young',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NathanY3G/CircuitPython_Unicorn_HAT_HD',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
