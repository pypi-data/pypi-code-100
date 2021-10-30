import os

from setuptools import find_packages, setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as file:
        return file.read()


setup(
    name="grebarss",
    version="4.1.12",
    author="Alexander Hreben",
    author_email="greba3000@gmail.com",
    url="https://github.com/Greba3000/Homework",
    description="CLI utility for reading news",
    # long_description=read("README.md"),
    python_requires=">=3.9",
    classifiers=["Programming Language :: Python :: 3.9"],
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt").splitlines(),
    entry_points={
        "console_scripts": [
            "grebarss=grebarss_reader.rss_reader:main",
            "rss_reader=grebarss_reader.rss_reader:main",
        ],
    },
)