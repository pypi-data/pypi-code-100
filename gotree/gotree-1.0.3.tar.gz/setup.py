from setuptools import find_packages,setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gotree", #模块名
    version="1.0.3",#版本
    packages=find_packages(),#目录所有文件
    author="Newman Lv",#作者名
    author_email="453276749@qq.com",
    description="A new solution to tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.baidu.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

