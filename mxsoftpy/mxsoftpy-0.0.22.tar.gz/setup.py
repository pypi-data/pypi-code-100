# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='mxsoftpy',
    version='0.0.22',
    author='great',
    author_email='great@mxsoft.com',
    url='https://gitee.com/yuanhao_1998/mxsoftpy.git',
    description=u'美信python框架',
    packages=find_packages(),
    install_requires=['pydantic', 'typing-extensions'],
    entry_points={}
)
