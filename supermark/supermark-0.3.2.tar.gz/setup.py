from distutils.core import setup
from pathlib import Path


def get_version(path: str) -> str:
    for line in Path(path).read_text().splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


package_name = "supermark"

setup(
    name=package_name,
    packages=[
        package_name,
        "supermark.extensions",
        "supermark.extensions.abstract",
        "supermark.extensions.boxes",
        "supermark.extensions.button",
        "supermark.extensions.check",
        "supermark.extensions.code",
        "supermark.extensions.definition",
        "supermark.extensions.delivery",
        "supermark.extensions.double",
        "supermark.extensions.figure",
        "supermark.extensions.goals",
        "supermark.extensions.guideline",
        "supermark.extensions.hints",
        "supermark.extensions.lines",
        "supermark.extensions.rat",
        "supermark.extensions.report",
        "supermark.extensions.rubrics",
        "supermark.extensions.steps",
        "supermark.extensions.table",
        "supermark.extensions.task",
        "supermark.extensions.tips",
        "supermark.extensions.tree",
        "supermark.extensions.video",
        "supermark.extensions.warning",
        "supermark.extensions.weekplan",
    ],
    version=get_version("{}/__init__.py".format(package_name)),
    description="Pandoc-based transformation tool for documents containing different markup languages.",
    # long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires=[
        "pypandoc",
        "pyyaml",
        "click",
        "openpyxl",
        "progressbar2",
        "pygments",
        "wikitextparser",
        "requests",
        "cairosvg",
        "pathlib",
        "tqdm",
        "indentation",
        "blindspin",
        # "beepy",
        "watchdog",
        "pretty_errors",
        "rich",
        "icecream",
        "black",
        "blindspin",
    ],
    package_data={
        "": ["*.tex", "*.pdf", "*.css", "*.md"],
    },
    include_package_data=True,
    author="Frank Alexander Kraemer",
    author_email="kraemer.frank@gmail.com",
    license="GPLv3",
    url="https://github.com/falkr/supermark",
    download_url="https://github.com/falkr/supermark/archive/0.2.tar.gz",
    keywords=["education"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"console_scripts": ["supermark=supermark.command:supermark"]},
)
