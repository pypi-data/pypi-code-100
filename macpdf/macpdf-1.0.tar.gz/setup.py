import setuptools
from pathlib import Path


setuptools.setup(
    # find the package to install and exclude tests and data
    name="macpdf",
    version=1.0,
    description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    license="LICENSE"
)
