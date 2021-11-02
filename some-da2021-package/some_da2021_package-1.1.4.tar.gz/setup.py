from setuptools import setup

setup(
    name='some_da2021_package',
    version='1.1.4',  
    url='https://github.com/lejabque',
    description='A example Python package',
    author='Denis Vorkozhokov',
    author_email='vorkdenis1@gmail.com',
    license='MIT',
    packages=['some_da2021_package'],
    install_requires=['numpy==1.16.0', 'scipy==1.7.1'],
)
