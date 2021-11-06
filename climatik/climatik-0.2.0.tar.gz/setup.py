import pathlib
from setuptools import setup
from climatik import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="climatik",
    version=__version__,
    description="Create command line interface from function definitions.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://git.sr.ht/~fabrixxm/climatik",
    author="Fabio Comuni",
    author_email="fabrix.xm+pypi@gmail.com",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["climatik"],
)
