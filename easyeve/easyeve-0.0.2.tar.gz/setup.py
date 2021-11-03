#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages


VERSION = input("Input the new version number you are going to use: ")

setup(name='easyeve',
      version=VERSION,
      description="maiff tools",
      long_description='just enjoy',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='maiff easyeve terminal',
      author='maiff',
      author_email='xwt2101239@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts':[
            'easyeve = easyeve.main:main'
        ]
      },
)