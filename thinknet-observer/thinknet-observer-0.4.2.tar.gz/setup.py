# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# long_description = ""
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# with open(path.join(HERE, "CHANGELOG.txt"), encoding="utf-8") as f:
#     long_description += "\n\n" + f.read()
# TODO read at : https://pythonpackaging.info/07-Package-Release.html and
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
# for info about changelog implementation

# This call to setup() does all the work
setup(
    name="thinknet-observer",
    version="0.4.2",
    description="lib in development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.thinknet.co.th/big-data/thinknet-observer-python",
    author="TN - DS Team",
    author_email="nattawutd@thinknet.co.th",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "numpy == 1.21.2",
        "prometheus-client == 0.11.0",
        "Flask",
        "fastapi",
    ],
)
