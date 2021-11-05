# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='itle',
      version='0.1.2',
      description='接口包装库',
      long_description='B端工程staking的api接口包装库',
      license='MIT Licence',
      author='coz',
      author_email='364247556@qq.com',
      namespace_packages=['itle', ],
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      install_requires=[  # 安装依赖的其他包（测试数据）
          'aiohttp~=3.8.0',
      ],
      url="https://gitee.com/coz2021/itle",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ], )
