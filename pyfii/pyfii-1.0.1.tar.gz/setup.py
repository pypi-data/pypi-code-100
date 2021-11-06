from setuptools import setup

setup(
    name='pyfii',
    version='1.0.1',
    author='ZKevinHU',
    url='https://www.bilibili.com/video/BV1Eh411t7NW',
    description=u'用python编写Fii无人机程序并预览',
    long_description=u'这个库的功能是可以让我们用python写Fii的无人机程序，以解决原软件无运算能力，无循环模块，一块块拖太烦等问题。此外，这个库有三视图模拟飞行的功能，模拟飞行更方便观看。',
    packages=['pyfii'],
    install_requires=['opencv-python']
)
