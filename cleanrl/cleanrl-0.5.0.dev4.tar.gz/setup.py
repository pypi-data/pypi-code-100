# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleanrl_utils']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.21.0,<0.22.0',
 'opencv-python>=4.5.3,<5.0.0',
 'pyglet>=1.5.19,<2.0.0',
 'tensorboard>=2.5.0,<3.0.0',
 'torch>=1.9.0,<2.0.0',
 'wandb>=0.12.1,<0.13.0']

extras_require = \
{'atari': ['stable-baselines3>=1.1.0,<2.0.0',
           'ale-py>=0.7,<0.8',
           'AutoROM[accept-rom-license]>=0.4.2,<0.5.0'],
 'cloud': ['boto3>=1.18.57,<2.0.0', 'awscli>=1.20.57,<2.0.0'],
 'docs': ['mkdocs-material>=7.3.4,<8.0.0'],
 'mujoco': ['free-mujoco-py>=2.1.6,<3.0.0'],
 'pettingzoo': ['stable-baselines3>=1.1.0,<2.0.0',
                'pettingzoo>=1.11.2,<2.0.0',
                'pygame>=2.0.1,<3.0.0',
                'pymunk>=6.2.0,<7.0.0'],
 'plot': ['pandas>=1.3.3,<2.0.0', 'seaborn>=0.11.2,<0.12.0'],
 'procgen': ['stable-baselines3>=1.1.0,<2.0.0', 'procgen>=0.10.4,<0.11.0'],
 'pybullet': ['pybullet>=3.1.8,<4.0.0'],
 'pytest': ['pytest>=6.2.5,<7.0.0'],
 'spyder': ['spyder>=5.1.5,<6.0.0']}

setup_kwargs = {
    'name': 'cleanrl',
    'version': '0.5.0.dev4',
    'description': 'High-quality single file implementation of Deep Reinforcement Learning algorithms with research-friendly features',
    'long_description': None,
    'author': 'Costa Huang',
    'author_email': 'costa.huang@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
