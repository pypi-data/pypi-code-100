import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="hwpfc",
    version="0.0.3",
    description="Hello word from pfc",
    packages=["hwpfc"],
    install_requires=["feedparser", "html2text"],
    entry_points={
        "console_scripts": [
            "hwpfc=hwpfc.__main__:main",
        ]
    },
)