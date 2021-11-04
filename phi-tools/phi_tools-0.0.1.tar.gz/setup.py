# -*- ecoding: utf-8 -*-
# @ModuleName: setup
# @Function: 
# @Author: ctx_phi
# @Craete Time: 2021/11/4 10:51


import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="phi_tools",
  version="0.0.1",
  author="phimes",
  author_email="phimes@163.com",
  description="A collections of often use functions",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/re0phimes/phi-s_ultis",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)