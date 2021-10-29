from setuptools import find_packages
from setuptools import setup

VERSION = '0.1.2'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='vkinfo',
    url='https://github.com/Addic7edBoy/ImprovadoTest',
    author='Max Medvedev',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=[
        'requests>=2.26.0',
        'pandas>=1.3.3',
        'six>=1.16.0',
        'httpretty>=1.1.4',
        'responses>=0.14.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=('''VK users data analyzer'''),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['vkinfo=vkinfo.__main__:main'],
    }
)