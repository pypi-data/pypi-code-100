# coding:utf-8
from setuptools import setup, find_packages
import sys


# def get_requirements():
#     with open('requirements.txt') as requirements:
#         des_pkg = [line.split('#', 1)[0].strip() for line in requirements
#                    if line and not line.startswith(('#', '--'))]
#         return des_pkg


setup(
    name='rpc_common',         # 应用名
    version='0.0.9',       # 版本号
    author='zhengshuiqing',
    author_email='zhengshuiqing@goldwind.com.cn',
    description='rpc服务端和客户端使用的公共文件',
    license='Private',
    include_package_data=True,
    install_requires=[
        "grpcio==1.37.1",
        "grpcio-tools==1.37.1",
        "protobuf==3.17.0"
    ],
    packages=find_packages(exclude=['examples', 'tests']),    # 包括在安装包内的Python包
    test_suite="tests",
    dependency_links=['https://pypi.tuna.tsinghua.edu.cn/simple']
)
