import setuptools
from pathlib import Path

setuptools.setup(
    name="lempdf",
    version=2.2,
    long_description=Path("README.md").read_text(),
    # find packages that we define and exclude dir tests and data
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
