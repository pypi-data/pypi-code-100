"""trading-strategies is the Quant Team's Strategy Python Library
and is a core part of our crypto-asset trading bots.
"""

from __future__ import annotations

from setuptools import setup
from setuptools import find_namespace_packages


DOCLINES = __doc__.split("\n")


def requirements() -> list[str]:
    with open("requirements/base.txt", "r") as file_handler:
        package_list = file_handler.readlines()
        package_list = [package.rstrip() for package in package_list]

    return package_list


setup(
    name="trading.backtester",
    description=DOCLINES[0],
    author="SwapooLabs Quantitative Developers",
    version="1.2.0",

    install_requires=requirements(),
    packages=find_namespace_packages(include=[
        "trading.*",
    ]),
    python_requires=">=3.7"
)
