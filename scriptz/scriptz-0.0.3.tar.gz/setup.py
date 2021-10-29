import re
from os import path
from pathlib import Path

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    version = Path(package, "__version__.py").read_text()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", version).group(1)


def get_long_description():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


install_requires = [
    "typer>=0.3.2",
    "rich>=10.0.0",
]

setup(
    name="scriptz",
    python_requires=">=3.6",
    version=get_version("src/scriptz"),
    author="Ian Maurer",
    author_email="ian@genomoncology.com",
    packages=find_packages("src/"),
    package_dir={"": "src"},
    package_data={"": ["scriptz.ini"]},
    include_package_data=True,
    entry_points={
        "console_scripts": ["scriptz=scriptz:cli", "sz=scriptz:cli"]
    },
    install_requires=install_requires,
    description="CLI tool for managing sequential script execution.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/genomoncology/scriptz",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
)
