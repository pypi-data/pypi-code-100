import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

version_path = HERE / "jerome" / "__version__.py"
with open(version_path, "r") as fh:
    version_dict = {}
    exec(fh.read(), version_dict)
    VERSION = version_dict["__version__"]

print(VERSION)

setup(
    name="jerome",
    version=VERSION,
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=("String Processing Tools"),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kajuberdut/jerome",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
