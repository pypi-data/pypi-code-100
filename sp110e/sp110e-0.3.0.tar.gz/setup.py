# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sp110e']

package_data = \
{'': ['*']}

install_requires = \
['bleak==0.13.0', 'syncer==1.3.0']

setup_kwargs = {
    'name': 'sp110e',
    'version': '0.3.0',
    'description': 'Control SP110E BLE RGB LED device from computer',
    'long_description': "# SP110E Python Library\n\nControl SP110E BLE RGB LED device from computer\n\n## Install\n\n```bash\npip install SP110E\n```\n\n## Tools\n\n- Controller: High-level SP110E asynchronous controller. Use it only in asynchronous environment (with `asyncio`) \n- **ControllerSync**: Synchronous adapter for high-level SP110E asynchronous controller. Handy tool to use from Python shell or synchronous (normal) environment\n- Driver: Low-level SP110E asynchronous BLE driver based on bleak library. Use it only if you're sure why.\n\n## Examples\n\n```python\nfrom SP110E.ControllerSync import ControllerSync\n\ndevice = ControllerSync()\ndevice.connect('AF:00:10:01:C8:AF')\ndevice.switch_on()\ndevice.set_color([255, 0, 0])\ndevice.set_brightness(255)\ndevice.disconnect()\n```\n\n## Useful links\n\n- [API Reference](https://gist.github.com/mbullington/37957501a07ad065b67d4e8d39bfe012)\n- [Vox](https://github.com/nguyenthuongvo/Vox)\n- [bleak library](https://github.com/hbldh/bleak)\n- [Reverse engineering simple BLE](http://nilhcem.com/iot/reverse-engineering-simple-bluetooth-devices)\n",
    'author': 'Pavel Roslovets',
    'author_email': 'p.v.roslovets@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roslovets/SP110E',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
