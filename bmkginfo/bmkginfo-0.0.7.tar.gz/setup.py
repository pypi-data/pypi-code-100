import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmkginfo",
    version="0.0.7",
    author="Endang Ismaya",
    author_email="endang.ismaya@gmail.com",
    description="BMKGINFO is a Python library for getting information about latest earth quake and wheather forecast in Indonesia base on BMKG | Meteorological, Climatological, and Geophysical Agency Website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/endang-ismaya/bmkginfo",
    project_urls={
        "Bug Tracker": "https://github.com/endang-ismaya/bmkginfo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    packages=setuptools.find_packages(),
    install_requires=["requests", "beautifulsoup4"],
    python_requires=">=3.6",
)
