#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

# python setup.py sdist 打包成tar.gz的形式
# python setup.py bdist_wheel  打包成wheel格式

setup(
    py_modules=["train"],  # 需要打包的文件夹下的py文件名词cal_similarity.py
    packages=find_packages(),  # 需要打包的目录列表
    name="kflearn",  # 包名称，也就是文件夹名称
    version="1.0.0",  # 包的版本
    description="kubeflow machine learning kit",  # 对当前package的较短总结
    long_description="kubeflow machine learning kit",  # 对当前package的详细说明
    author="horn",  # 作者姓名
    author_email="hongen26@163.com",  # 作者邮箱
    install_requires=['numpy'],  # 第三方依赖,这些依赖包会在程序安装的时候也会安装
    zip_safe=False,  # 此项需要，否则卸载报windows error错误
    license="MIT Licence",  # 支持的开源协议
    python_requires=">=3.6.0",  # 指定python的安装要求
    include_package_data=True
)
