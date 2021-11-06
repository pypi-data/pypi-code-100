import setuptools
from distutils.core import setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("hanlab/version.py", "r") as f:
    # Define __version__
    exec(f.read())

setup(
    name="hanlab",
    packages=setuptools.find_packages(),
    version=__version__,
    license="MIT",
    description="hanlab - odnp data processing and fitting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thomas Casey",
    url="https://github.com/thcasey3/hanlab",
    download_url="https://github.com/thcasey3/hanlab/",
    project_urls={
        "Homepage": "https://thcasey3.github.io/hanlab/",
        "Documentation": "https://thcasey3.github.io/hanlab/",
        "Source": "https://github.com/thcasey3/hanlab/",
    },
    keywords=["dnplab odnp nmr epr dnp"],
    python_requires=">=3.6",
    install_requires=[
        "dnplab",
        "numpy",
        "scipy",
        "PyQt5",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points=dict(
        console_scripts=[
            "hydrationGUI=hanlab.hydrationGUI:main_func",
        ]
    ),
)
