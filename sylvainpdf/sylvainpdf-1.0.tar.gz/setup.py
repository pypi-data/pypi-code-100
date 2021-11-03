import setuptools
from pathlib import Path

setuptools.setup(
    name="sylvainpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude = ["tests","data"]) #Will take all packages we have created in the directory except 2 that have no source code
)