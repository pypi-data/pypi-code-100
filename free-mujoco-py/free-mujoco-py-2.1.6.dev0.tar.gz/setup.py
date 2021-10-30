# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mujoco_py',
 'mujoco_py.generated',
 'mujoco_py.gl',
 'mujoco_py.pxd',
 'mujoco_py.tests']

package_data = \
{'': ['*'],
 'mujoco_py': ['binaries/linux/mujoco210/*',
               'binaries/linux/mujoco210/bin/*',
               'binaries/linux/mujoco210/include/*',
               'binaries/linux/mujoco210/model/*',
               'binaries/linux/mujoco210/sample/*',
               'binaries/macos/mujoco210/*',
               'binaries/macos/mujoco210/bin/*',
               'binaries/macos/mujoco210/include/*',
               'binaries/macos/mujoco210/model/*',
               'binaries/macos/mujoco210/sample/*',
               'binaries/windows/mujoco210/*',
               'binaries/windows/mujoco210/bin/*',
               'binaries/windows/mujoco210/include/*',
               'binaries/windows/mujoco210/model/*',
               'binaries/windows/mujoco210/sample/*',
               'test_imgs/*']}

install_requires = \
['Cython>=0.29.24,<0.30.0',
 'cffi>=1.15.0,<2.0.0',
 'fasteners==0.15',
 'glfw>=1.4.0,<2.0.0',
 'imageio>=2.9.0,<3.0.0',
 'numpy>=1.21.3,<2.0.0']

setup_kwargs = {
    'name': 'free-mujoco-py',
    'version': '2.1.6.dev0',
    'description': '',
    'long_description': None,
    'author': 'Costa Huang',
    'author_email': 'costa.huang@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
