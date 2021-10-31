import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
VERSION = "1.1.0"
REQUIREMENTS = (HERE / "requirements.txt").read_text()
REQUIREMENTS = REQUIREMENTS.split('\n')

setup(
    name = "sortz",
    version = VERSION,
    description = "Visualize sorting algorithms",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/MdeVillefort/sortz",
    author = "Monsieur de Villefort",
    author_email = "ethanmross92@gmail.com",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages = ["sortz"],
    install_requires = REQUIREMENTS,
    entry_points = {
        "console_scripts" : [
            "sortz-cli=sortz.__main__:main"
        ]
    },
)