import sys

from setuptools import setup, find_packages
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("sdist")
parser.add_argument("bdist_wheel")
parser.add_argument("--version", default="0.0.0")
options = parser.parse_args(sys.argv[1:])

new_argv = []
for argv in sys.argv:
    if not argv.startswith("--version"):
        new_argv.append(argv)

sys.argv = new_argv


setup(
    name="levatas-alira-cli",
    version=options.version,
    description="Alira CLI",
    url="https://github.com/vinsa-ai/alira-cli",
    author="Levatas",
    author_email="svpino@gmail.com",
    packages=find_packages(exclude=["license", "libs"]),
    include_package_data=True,
    install_requires=["Click", "Docker", "python-dateutil", "levatas-alira-licensing"],
    entry_points={
        "console_scripts": [
            "alr = alira_cli.alr:cli",
        ],
    },
)
