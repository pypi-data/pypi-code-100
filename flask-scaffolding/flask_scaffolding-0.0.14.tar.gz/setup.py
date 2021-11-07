import os
import shutil
import setuptools
from distutils import sysconfig


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_scaffolding",
    version="0.0.14",
    author="Muhammad Yunus",
    author_email="yunusmuhammad007@gmail.com",
    description="Flask Scaffolding with buiiltin Authentication & Authorization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Muhammad-Yunus/Flask-Scaffolding-Base",
    project_urls={
        "Bug Tracker": "https://github.com/Muhammad-Yunus/Flask-Scaffolding-Base/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    package_data={
        'scaffold': ['base/instance/*.py', 
                     'base/app/**/*.html', 
                     'base/app/**/**/*.html', 
                     'base/app/**/**/*.css']
        },
    python_requires=">=3.6"
)