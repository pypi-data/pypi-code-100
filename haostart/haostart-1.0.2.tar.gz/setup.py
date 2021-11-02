from __future__ import print_function
from setuptools import setup

setup(
    name="haostart",
    version="1.0.2",
    author="haostart",
    author_email="haostart@hotmail.com",
    description="Haostart-Self_Tools",
    long_description=open("README.md", encoding='utf-8').read(),
    license="Apache License",
    url="https://gitee.com/haostart/dashboard/projects",
    packages=['haostart'],
    install_requires=[
        'requests',


    ],

)
