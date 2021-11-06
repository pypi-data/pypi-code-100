from setuptools import setup, find_packages
import shitage.consts as const


setup(name='shitage',
version=const.VERSION,
description=const.DESC,
author='pipd0un',
author_email='pipdoun@gmail.com',
license='MIT',
packages=find_packages(),
install_requires=['os','subprocess','sys'],
keywords=['netsh','WLAN','passwords'],
classifiers=["Intended Audience :: Education",
             "Programming Language :: Python :: 3",
             "Operating System :: Microsoft :: Windows",],
zip_safe=False)