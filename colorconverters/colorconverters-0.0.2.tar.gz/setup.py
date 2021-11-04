from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='colorconverters',
    version='0.0.2',
    description='Handles colors and features various other utilities related to color conversions',
    long_description=long_description,
    url='',
    author='GenZ Gamer',
    author_email='thatgenzgamer@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='colors, converters, colorconverters',
    packages=find_packages(),
    install_requires=['']
)
