"""Setup for Pytong."""
import setuptools  # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netqr",
    version="0.1.1",
    author="Richard Tong",
    author_email="rich@netdron.es",
    description="Rich Tong's Fine QR Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netdrones/qr",
    # include additional files where py.typed is the magic
    # indication of inline type annotations with an empty file named py.typed
    # https://blog.ian.stapletoncordas.co/2019/02/distributing-python-libraries-with-type-annotations.html
    # https://www.python.org/dev/peps/pep-0561/
    package_data={"netqr": ["py.typed"]},
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    # https://www.geeksforgeeks.org/command-line-scripts-python-packaging/
    # ./scripts/main.py is the command line entry point
    # use entry points if you want to call functions that are directly in the
    # package
    # entry_points={"console_scripts": ["qr = src.netpy.main:main"]},
    # use scripts to run code that calls the package and which are named
    # properly
    scripts=["bin/qr.py"],
    project_urls={
        "Bug Tracker": "https://github.com/netdrones/qr/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
