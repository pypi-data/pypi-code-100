#!/usr/bin/python3

from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name='setuptools-cmake',
    version='1.0',
    author='TheClockTwister',
    description='A setuptools intrgration for CMake built extension modules',
    long_description=long_description,
    packages=find_packages(),
    package_data={
        '': ['CMakeLists.txt'
             ],
    },
    install_requires=['pybind11[global]', 'click', 'colorama'],
    entry_points={  # CLI scripts
        'console_scripts': [
            # 'setuptools-cmake = setuptools_cmake:init',
        ],
    },
)
